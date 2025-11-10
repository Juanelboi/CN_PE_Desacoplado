# Dockerfile (Para la Versión Desacoplada - Lambda)
FROM public.ecr.aws/lambda/python:3.11

# Establecer el directorio de trabajo
WORKDIR ${LAMBDA_TASK_ROOT}

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY ./app/ ./app/

# El handler se especificará mediante ImageConfig.Command en el template.yml