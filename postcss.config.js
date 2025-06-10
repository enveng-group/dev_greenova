import autoprefixer from 'autoprefixer';
import postcssPresetEnv from 'postcss-preset-env';

export default {
  plugins: [
    autoprefixer,
    postcssPresetEnv({
      stage: 1,
      features: {
        'nesting-rules': true
      }
    })
  ]
};
