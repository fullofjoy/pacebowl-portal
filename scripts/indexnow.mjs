#!/usr/bin/env node
/**
 * Automated IndexNow Submitter for PaceBowl Studio (https://pacebowl.com)
 * Submits all 7 apex domain URLs to IndexNow network (Bing, Yandex, Naver, Seznam).
 */

import https from 'node:https';

const HOST = 'pacebowl.com';
const KEY = 'c89e21f47b6a4f90918237d04ea38971';
const KEY_LOCATION = `https://${HOST}/${KEY}.txt`;

const URL_LIST = [
  `https://${HOST}/`,
  `https://${HOST}/tools/cursor-rules-generator/`,
  `https://${HOST}/tools/comfyui-latent-calculator/`,
  `https://${HOST}/tools/moe-vram-estimator/`,
  `https://${HOST}/tools/deepseek-prompt-studio/`,
  `https://${HOST}/tools/open-geo-attribution/`,
  `https://${HOST}/tools/reddit-growth-studio/`
];

const ENDPOINTS = [
  { name: 'IndexNow Global (api.indexnow.org)', hostname: 'api.indexnow.org', path: '/indexnow' },
  { name: 'Bing IndexNow (www.bing.com)', hostname: 'www.bing.com', path: '/indexnow' }
];

function submitToIndexNow(endpoint, payload) {
  return new Promise((resolve) => {
    const data = JSON.stringify(payload);
    const options = {
      hostname: endpoint.hostname,
      port: 443,
      path: endpoint.path,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': Buffer.byteLength(data),
      },
      timeout: 10000,
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => (body += chunk));
      res.on('end', () => {
        if (res.statusCode === 200 || res.statusCode === 202) {
          console.log(`✅ [IndexNow] ${endpoint.name} accepted submission (HTTP ${res.statusCode})`);
          resolve(true);
        } else {
          console.warn(`⚠️ [IndexNow] ${endpoint.name} responded HTTP ${res.statusCode}: ${body || 'No message'}`);
          resolve(false);
        }
      });
    });

    req.on('error', (err) => {
      console.error(`❌ [IndexNow] Error with ${endpoint.name}:`, err.message);
      resolve(false);
    });

    req.write(data);
    req.end();
  });
}

async function main() {
  console.log(`🚀 [IndexNow] Submitting ${URL_LIST.length} URLs to IndexNow endpoints for ${HOST}...`);
  const payload = {
    host: HOST,
    key: KEY,
    keyLocation: KEY_LOCATION,
    urlList: URL_LIST,
  };

  for (const endpoint of ENDPOINTS) {
    await submitToIndexNow(endpoint, payload);
  }

  console.log(`🎉 [IndexNow] Push complete for ${URL_LIST.length} URLs!`);
}

main();
