import requests

url = 'http://127.0.0.1:5000'
data = {"text": """Time management is a crucial skill that influences both personal and professional success. In today’s fast-paced world, the ability to effectively allocate and use time can mean the difference between achieving goals and falling behind.

One of the key reasons time management is so important is that time is a limited resource. Unlike money or material possessions, once time passes, it cannot be regained. This makes it vital to prioritize tasks and allocate appropriate time for each activity. By organizing time efficiently, individuals can focus on what matters most, reducing stress and avoiding the last-minute rush to meet deadlines.

Effective time management leads to higher productivity. When individuals break their work into manageable chunks and set specific goals for each period, they tend to accomplish more. It helps to eliminate distractions and stay focused on the task at hand. Moreover, with a clear plan, people are less likely to procrastinate, which is a common barrier to productivity."""}

response = requests.post(url, json=data)
print(response.json())
