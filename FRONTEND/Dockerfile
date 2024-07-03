# Utiliza a imagem oficial do Node.js como base
FROM node:16-alpine

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o package.json e o package-lock.json para o diretório de trabalho
COPY package*.json ./

# Instala as dependências do projeto
RUN npm install

# Copia todo o código-fonte do projeto para o diretório de trabalho
COPY . .

# Expõe a porta que o servidor de desenvolvimento usa
EXPOSE 3000

# Comando para iniciar o servidor de desenvolvimento
CMD ["npm", "run", "build"]
