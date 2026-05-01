/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*', // Proxy to backend
      },
      {
        source: '/health',
        destination: 'http://localhost:8000/health', // Proxy health check
      },
    ];
  },
};

module.exports = nextConfig;
