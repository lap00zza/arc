var del = require("del");
var path = require("path");
var gulp = require("gulp");
var sass = require("gulp-sass");
var gutil = require("gulp-util");
var webpack = require("webpack");
var runSequence = require("run-sequence");

gulp.task("webpack", function (callback) {
    webpack({
        entry: {
            core: path.resolve(__dirname, "client/src/assets/js/core.js")
        },
        output: {
            filename: "[name].bundle.js",
            path: path.resolve(__dirname, "client/src/assets/build")
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
    return gulp.src("client/src/assets/sass/*.sass")
        .pipe(sass())
        .pipe(gulp.dest("client/src/assets/build"));
});

// Build the sass and the JS files.
gulp.task("build", function () {
    runSequence("webpack", "sass")
});
