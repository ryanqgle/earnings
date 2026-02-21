import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:3000/:path*",
      },
      {
        source: "/api",
        destination: "http://localhost:3000/",
      },
    ];
  },
};

export default nextConfig;