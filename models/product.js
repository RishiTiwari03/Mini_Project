
const mongoose = require('mongoose');


// Define a schema (no default `_id`, custom `id` as unique identifier)
const productSchema = new mongoose.Schema(
    {
        id: { type: Number, required: true, unique: true },
        gender: String,
        masterCategory: String,
        subCategory: String,
        articleType: String,
        baseColour: String,
        season: String,
        price: Number,
        link: String,
        productDisplayName: String,
    },
    { _id: false } // Disable default `_id` field
);

const Product = mongoose.model('Product', productSchema);
module.exports = Product;