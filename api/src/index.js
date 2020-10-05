import express from 'express';
import puppeteer from 'puppeteer-core';

const app = express();
const port = 3000;

app.use(express.urlencoded({extended: true}));
app.use(express.json());

app.post('/', async (req, res) => {
  const browser = await puppeteer.connect({browserURL: 'http://chrome:3001'});
  const page = await browser.newPage();
  await page.setContent(req.body);
  const pdf = await page.pdf({ format: 'a4' });
  await browser.close();
  res.set({ 'Content-Type': 'application/pdf', 'Content-Length': pdf.length });
  res.send(pdf);
})

app.listen(port, () => console.log(`Server running at http://localhost:${port}`));
