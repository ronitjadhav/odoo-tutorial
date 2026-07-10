import { createMDX } from 'fumadocs-mdx/next';

const withMDX = createMDX();

/** @type {import('next').NextConfig} */
const config = {
  output: 'export',
  // served at https://ronitjadhav.github.io/odoo-tutorial/
  basePath: '/odoo-tutorial',
  trailingSlash: true,
  reactStrictMode: true,
};

export default withMDX(config);
