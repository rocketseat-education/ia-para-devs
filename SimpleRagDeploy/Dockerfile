# Use the AWS base image for python 3.12
FROM public.ecr.aws/lambda/python:3.12

# Install build-essencial compiler and tools
RUN microdnf update -y && microdnf install -y gcc-c++ make

# COPY the requirements.txt file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the libs in requirements.txt file
RUN pip install -r requirements.txt

# COPY the requirements.txt file
COPY DOC-SF238339076816-20230503.pdf ${LAMBDA_TASK_ROOT}/DOC-SF238339076816-20230503.pdf

# Copy the function code
COPY simplerag.py ${LAMBDA_TASK_ROOT}

# Set permission to make the file executable
RUN chmod +x simplerag.py

# Set CMD to your handler

CMD ["simplerag.lambda_handler"]
