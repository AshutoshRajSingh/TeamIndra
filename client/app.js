const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");
const app = express();

app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static("public"));
app.set("view engine","ejs");

var labels = []
var styles = {}

app.get("/",function(req,res){
   
    
    res.render("index");

})

app.post("/", function(req,res){
    const state = req.body["state"];
    const url = "http://localhost:8000/api/states/"+state+"/";
    axios.get(url).then(function(response){
        let apiData = response.data
        const surplus = apiData.data.monthly_availability - apiData.data.predicted_monthly_usage;

        apiData.data["timestamps"].forEach((date)=>{
            var d = new Date(date*1000);
            var day = d.getDate();
            var month = d.getMonth();
            var year = d.getFullYear();
    
            date = year + '-' + month + '-' + day;
      
            labels.push(date);
        });

        if (surplus>=0){
            styles = {
                color : "green",
                message : "You're good to go 💡" 
            }
        }
        else{
            styles = {
                color : "red",
                message : "Oh oh. Looks like your state is about to run out of electricity 😞"
            }
        }
        res.render("results",{"state": state,"apiData":apiData,"labels":labels,"styles" : styles , "surplus":surplus});
    }) 
})

app.listen(3000,()=>{
    console.log("Server running on port 3000");
})