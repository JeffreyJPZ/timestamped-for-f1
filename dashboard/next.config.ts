import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  ignoreBuildErrors: true, // TODO: remove after fixing react-query typing
};

export default nextConfig;
