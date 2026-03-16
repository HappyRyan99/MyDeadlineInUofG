const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const iconsToExtract = [
  'people-fill', 'plus-lg', 'person-plus', 'person-fill', 'x-lg', 'trash', 
  'people', 'arrow-left', 'person-circle', 'calendar3', 'clock-fill', 'dot', 
  'card-checklist', 'check2-circle', 'check-circle-fill', 'check-lg', 'pencil', 
  'clock', 'check2-all', 'exclamation-circle', 'journal-text', 'exclamation-triangle', 
  'clock-history', 'speedometer2', 'book', 'box-arrow-right', 'calendar-check', 'calendar-event'
];

const iconsDir = path.join(__dirname, 'node_modules', 'bootstrap-icons', 'icons');
const outputFile = path.join(__dirname, 'src', 'assets', 'icons.js');

const iconData = {};

iconsToExtract.forEach(name => {
  const filePath = path.join(iconsDir, `${name}.svg`);
  if (fs.existsSync(filePath)) {
    const svgContent = fs.readFileSync(filePath, 'utf8');
    const dom = new JSDOM(svgContent);
    const svgElement = dom.window.document.querySelector('svg');
    iconData[name] = svgElement.innerHTML.trim();
  } else {
    console.warn(`Icon ${name} not found at ${filePath}`);
  }
});

const fileContent = `export const icons = ${JSON.stringify(iconData, null, 2)};\n`;
fs.writeFileSync(outputFile, fileContent);
console.log(`Successfully extracted ${Object.keys(iconData).length} icons to ${outputFile}`);
