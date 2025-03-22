FROM node:18

WORKDIR /app

# Install dependencies for pcap and raw-socket
RUN apt-get update && apt-get install -y \
    libpcap-dev \
    python3 \
    make \
    g++

# Copy package.json and package-lock.json
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Command to run your application
CMD ["node", "app.js"]