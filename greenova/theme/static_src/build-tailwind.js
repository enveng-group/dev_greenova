// Custom tailwind build script for Tailwind CSS v4
const fs = require('fs');
const path = require('path');
const postcss = require('postcss');
const tailwindcssPostcss = require('@tailwindcss/postcss');
const autoprefixer = require('autoprefixer');

const inputPath = path.join(__dirname, 'src/styles.css');
const outputPath = path.join(__dirname, '../static/css/dist/styles.css');
// Additional output path for easier access via Django static files
const staticOutputPath = path.join(__dirname, '../../static/css/tailwind.css');

// Create output directories if they don't exist
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}
const staticOutputDir = path.dirname(staticOutputPath);
if (!fs.existsSync(staticOutputDir)) {
  fs.mkdirSync(staticOutputDir, { recursive: true });
}

// Read the input CSS file
fs.readFile(inputPath, (err, css) => {
  if (err) {
    console.error('Error reading input file:', err);
    process.exit(1);
  }

  // Process the CSS with PostCSS and plugins
  postcss([
    tailwindcssPostcss({
      config: path.join(__dirname, 'tailwind.config.js'),
    }),
    autoprefixer,
  ])
    .process(css, { from: inputPath, to: outputPath })
    .then((result) => {
      // Write the processed CSS to the output files
      fs.writeFile(outputPath, result.css, (err) => {
        if (err) {
          console.error('Error writing output file:', err);
          process.exit(1);
        }
        console.log(`Tailwind CSS built successfully to ${outputPath}`);

        // Write to the additional static file location
        fs.writeFile(staticOutputPath, result.css, (err) => {
          if (err) {
            console.error('Error writing static output file:', err);
            process.exit(1);
          }
          console.log(`Tailwind CSS also copied to ${staticOutputPath}`);
        });
      });
    })
    .catch((err) => {
      console.error('Error processing CSS:', err);
      process.exit(1);
    });
});
