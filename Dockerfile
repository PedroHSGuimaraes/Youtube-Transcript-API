FROM python:3.13-alpine
# Or any preferred Python version.
ADD main.py ./
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn","main:app"] 
# Or enter the name of your unique directory and parameter set.