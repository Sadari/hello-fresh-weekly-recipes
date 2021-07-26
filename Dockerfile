FROM python
COPY hello.py /opt/hello/hello.py
CMD ["python", "/opt/hello/hello.py"]
