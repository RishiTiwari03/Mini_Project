const express = require("express");
const app = express();
const path = require('path');
const ejsMate = require("ejs-mate");
const session = require("express-session");
const flash = require("connect-flash");
const passport = require("passport");
const LocalStrategy = require("passport-local")
const User = require("./models/user.js");
const mongoose = require('mongoose');
const methodOverride = require("method-override");
const { saveRedirectUrl } = require("./middleware.js");
const Product = require("./models/product.js");

app.engine("ejs", ejsMate); // Must be before app.set('view engine')
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static(path.join(__dirname, "/public")));
app.use(methodOverride("_method"));
app.use(express.urlencoded({ extended: true }));



async function main() {
    await mongoose.connect("mongodb://127.0.0.1:27017/mini_project")
}
main().then((res) => {
    console.log("connection established");
}).catch((err) => { console.log("connection is not successful "); });


const sessionOptions = {
    secret: "supersecretcode",
    resave: false,
    saveUninitialized: true,
    cookie: {
        expires: Date.now() + 7 * 24 * 60 * 60 * 1000,
        maxAge: 7 * 24 * 60 * 60 * 1000,
        httpOnly: true   //to avoid cross scripting attacks
    },
}
app.use(session(sessionOptions));
app.use(flash());

app.use(passport.initialize());
app.use(passport.session());
passport.use(new LocalStrategy(User.authenticate()));//telling passport konsi strategy use krni h
passport.serializeUser(User.serializeUser());// when user is logged in uski info store karani padhti h session me that is serializing user...taaki baar baar login na krna  pade..untill session is closed
passport.deserializeUser(User.deserializeUser());// when user is logged out uski  info unstore karani padhti h session me that is deserializing user

app.use((req, res, next) => {
    res.locals.success = req.flash("success");;
    res.locals.error = req.flash("error");
    res.locals.currentUser = req.user;
    next();

})




app.listen(3000, () => {
    console.log("on port 3000");
});


app.get("/", async(req, res) => {
    let allProducts = await Product.find({
        id: { $gte: 23100, $lte: 23120 }
    });
    // console.log(allProducts);
    
    res.render("templates/index",{allProducts})
});

app.get("/login", (req, res) => {  //home page login click
    res.render("user/login");
}) 

app.get("/signup", (req, res) => {  //home page signup click
    res.render("user/signup");
})

app.post("/signup", async (req, res) => {
    try {
        let { username, email, password } = req.body;
        const newUser = new User({ username, email });
        const registeredUser = await User.register(newUser, password)
        // console.log(registeredUser);
        req.logIn(registeredUser, (err) => {
            if (err) next(err);
            req.flash("success", `Welcome ${username}`)
            res.redirect("/")
        })

    } catch (e) {
        req.flash("error", "Account already Exists")
        res.redirect("/signup");
    }
})



app.post("/login",
    saveRedirectUrl,
    passport.authenticate("local", {
        failureRedirect: "/login",
        failureFlash: true,
    }),
    async (req, res) => {
        req.flash("success", `Logged in successfully ${req.body.username}`)
        redirectUrl = res.locals.redirectUrl;
        if (redirectUrl)
            return res.redirect(redirectUrl);
        res.redirect("/")
    });


app.get("/logout", (req, res, next) => {
    req.logOut((err) => {
        if (err) return next(err); //passport as a middleware agr fail hogya tb error askta h
        req.flash("success", "You are logged out")
        res.redirect("/")
    })
})

app.get('/blank',(req,res)=>{
    res.render("blank")
})