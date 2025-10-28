# Use Node.js official image (updated to support Vite 7)
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files from onus_client subdirectory
COPY onus_client/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY onus_client/ .

# Expose port 3000
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]