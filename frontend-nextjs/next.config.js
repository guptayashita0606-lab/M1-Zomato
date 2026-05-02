/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8004/api/:path*', // Proxy to backend
      },
      {
        source: '/health',
        destination: 'http://localhost:8004/health', // Proxy health check
      },
    ];
  },
};

module.exports = nextConfig;
