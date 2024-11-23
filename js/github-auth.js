// /.netlify/functions/github-auth.js
const fetch = require('node-fetch');

exports.handler = async (event) => {
  const clientId = process.env.GITHUB_CLIENT_ID;
  const clientSecret = process.env.GITHUB_CLIENT_SECRET;
  const code = event.queryStringParameters.code;

  // Exchange code for an access token
  const response = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify({ client_id: clientId, client_secret: clientSecret, code: code })
  });

  const data = await response.json();
  return {
    statusCode: 200,
    body: JSON.stringify(data)
  };
};


GITHUB_CLIENT_ID = Ov23lie5SbXF2hZcAHzJ

9f7bb2aa018c4f04ed8009f6e0598fe4f622a812


 9f7bb2aa018c4f04ed8009f6e0598fe4f622a812
API_KEY = your-api-key