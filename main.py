from fastapi import FastAPI
from pydantic import BaseModel
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.feature import Tokenizer, HashingTF, IDF, StringIndexer, CountVectorizer, VectorAssembler
import pandas as pd
from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
import openai
from openai import OpenAI

app = FastAPI()



class VideoData(BaseModel):
    video_title: str
    video_description: str
    video_tags: str
    video_trending_country: str






spark = SparkSession.builder.appName("VideoViralityPrediction").config("spark.hadoop.hadoop.native.io", "false").getOrCreate()


model_path = "lr_model"  
model = PipelineModel.load(model_path)


def predict_viral(video_data):
    video_data_with_defaults = {
        **video_data,
        "video_view_count": 0,
        "video_like_count": 0,
        "video_comment_count": 0,
    }
    
    df = spark.createDataFrame(pd.DataFrame([video_data_with_defaults]))
    
    predictions = model.transform(df)
    prediction_result = predictions.select("prediction").collect()[0][0]
    return bool(prediction_result)


@app.post("/predict-viral/")
def predict_viral_api(video: VideoData):
    video_dict = video.dict()
    prediction = predict_viral(video_dict)
    return {"is_viral": prediction}

# OpenAI API 
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def generate_title(topic):
    prompt = (
        f"You are a professional YouTube strategist. Given the topic below, "
        f"suggest 5 highly viral YouTube video titles under 70 characters.\n\n"
        f"Topic: {topic}\n\n"
        f"Return titles as a numbered list."
    )

    chat_completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for creating viral YouTube content."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
    )

    return chat_completion.choices[0].message.content

def generate_description(video_description):
    prompt = (
        f"You are a YouTube content expert. Given the video description below, "
        f"generate a highly engaging and compelling YouTube video description that encourages views. "
        f"Keep it under 200 characters.\n\n"
        f"Description: {video_description}\n\n"
        f"Return a description that is optimized for engagement and views."
    )

    chat_completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for optimizing YouTube content."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
    )

    return chat_completion.choices[0].message.content

@app.post("/generate/")
def generate_api(video: VideoData):
    new_title = generate_title(video.video_title)
    new_description = generate_description(video.video_description)

    return {
        "new_title": new_title,
        "new_description": new_description
    }