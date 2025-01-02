const fs = require('fs');
const csvParser = require('csv-parser');
const mongoose = require('mongoose');
const Product = require('../models/product.js');
// MongoDB connection

async function main() {
    await mongoose.connect("mongodb://127.0.0.1:27017/mini_project", {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    });
}
main().then((res) => {
    console.log("connection established");
}).catch((err) => { console.log("connection is not successful "); });


// Read and process the CSV file
const filePath = ('C:\\Users\\KIIT\\Desktop\\MINI_PROJECT\\initialize\\main.csv');

const jsonData = [];
fs.createReadStream(filePath)
    .pipe(csvParser())
    .on('data', (row) => {
        // Clean and transform the data
        const cleanedRow = {
            id: parseInt(row.id, 10),
            gender: row.gender,
            masterCategory: row.masterCategory,
            subCategory: row.subCategory,
            articleType: row.articleType,
            baseColour: row.baseColour,
            season: row.season,
            price: parseFloat(row.price.replace(/[^0-9.-]+/g, '')), // Remove ₹ and convert to a number
            link: row.link,
            productDisplayName: row.productDisplayName,
        };
        jsonData.push(cleanedRow);
        // console.log(jsonData);
    })
    .on('end', async () => {
        // Insert data into MongoDB
        await Product.deleteMany();
        console.log("DELETED");
        await new Promise(resolve => setTimeout(resolve, 5000));
        await Product.insertMany(jsonData)
            .then(() => {
                console.log('Data successfully imported into MongoDB');
                mongoose.connection.close();
            })
            .catch((error) => {
                console.error('Error inserting data:', error);
                mongoose.connection.close();
            });
    });
