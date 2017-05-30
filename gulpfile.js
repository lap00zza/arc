var del = require("del");
var path = require("path");
var gulp = require("gulp");
var sass = require("gulp-sass");
var gutil = require("gulp-util");
var webpack = require("webpack");
var runSequence = require("run-sequence");
var flatten = require("gulp-flatten");
var autoprefixer = require("gulp-autoprefixer");

gulp.task("webpack", function (callback) {
    webpack({
        entry: {
            core: path.resolve(__dirname, "nginx/client/core.js")
        },
        output: {
            filename: "[name].bundle.js",
            path: path.resolve(__dirname, "nginx/client/build")
        },
        module: {
          rules: [{
            test: /\.vue$/,
            loader: "vue-loader"
          }]
        },
        resolve: {
            alias: {
                "vue$": "vue/dist/vue.esm.js"
            }
        }
    }, function (err, stats) {
        if (err) throw new gutil.PluginError("webpack", err);
        gutil.log("[webpack]", stats.toString());
        callback();
    });
});

gulp.task("sass", function () {
    return gulp.src("nginx/client/assets/**/*.sass")
        .pipe(sass())
        .pipe(autoprefixer({
            cascade: false
        }))
        .pipe(flatten())
        .pipe(gulp.dest("nginx/client/build"));
});

// Build the sass and the JS files.
gulp.task("build", function () {
    runSequence("webpack", "sass")
});
