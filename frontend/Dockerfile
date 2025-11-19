# Use Node 20 as the base image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Expose the port
EXPOSE 5000

# Run the application
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5000"]