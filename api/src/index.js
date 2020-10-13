import express from 'express';
import puppeteer from 'puppeteer-core';
import DNS from 'dns';

const dns = DNS.promises;

const app = express();
const port = process.env.PORT || 3000;

const browserHost = process.env.BROWSER_HOST || 'chrome';

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.post('/', async (req, res) => {
  // dns lookup required to get around host header protections
  const lookup = await dns.lookup(browserHost);
  const options = req.body.options || {format: 'a4'};

  const browser = await puppeteer.connect({ browserURL: `http://${lookup.address}:3001` });
  const page = await browser.newPage();

  await page.setContent(req.body.data);
  const pdf = await page.pdf(options);
  await page.close();

  res.set({ 'Content-Type': 'application/pdf', 'Content-Length': pdf.length });
  res.send(pdf);
});

app.listen(port, () => console.log(`Server running at http://localhost:${port}`));
