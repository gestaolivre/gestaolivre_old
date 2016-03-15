/* global require, module */
var fs = require('fs');
var path = require('path');

var Angular2App = require('angular-cli/lib/broccoli/angular2-app');
var broccoliAutoprefixer = require('broccoli-autoprefixer');
var BroccoliSass = require('broccoli-sass');
var mergeTrees = require('broccoli-merge-trees');

var autoprefixerOptions = {
  browsers: [
    'last 2 versions',
    'not ie <= 10',
    'not ie_mob <= 10',
  ]
};

module.exports = function(defaults) {
  var appCssTree = new BroccoliSass(['src', 'src/styles', 'node_modules'], './styles.scss', 'styles.css');
  var appsCssTree = getCssTree('app');
  var app = new Angular2App(defaults, {
    vendorNpmFiles: [
      'ng2-material/**/*',
      'angular2-jwt/**/*',
      'jwt-decode/**/*'
    ]
  });

  return mergeTrees([
    app.toTree(),
    appCssTree,
    appsCssTree
  ]);
}

/** Gets the tree for all of the components' CSS. */
function getCssTree(folder) {
  var srcPath = `src/${folder}/`;
  var components = fs.readdirSync(srcPath)
    .filter(file => fs.statSync(path.join(srcPath, file)).isDirectory());

  var componentCssTrees = components.reduce((trees, component) => {
    // We want each individual scss file to be compiled into a corresponding css file
    // so that they can be individually included in styleUrls.
    var scssFiles = fs.readdirSync(path.join(srcPath, component))
        .filter(file => path.extname(file) === '.scss')
        .map(file => path.basename(file, '.scss'));

    return scssFiles.map(fileName => {
      return BroccoliSass(
          [`${srcPath}/${component}`], // Directories w/ scss sources
          `./${fileName}.scss`,                              // Root scss input file
          `${folder}/${component}/${fileName}.css`);        // Css output file
    }).concat(trees);
  }, []);
  return broccoliAutoprefixer(mergeTrees(componentCssTrees), autoprefixerOptions);
}
