const express = require("express");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());

let records = [];
let adminWarnings = {};

app.post("/addRecord", (req, res) => {
    const { adminId, name, email, phone } = req.body;

    if (!name || !email || !phone) {
        return res.status(400).json({ message: "Invalid data. All fields required." });
    }

    const duplicate = records.find(
        r => r.email === email || r.phone === phone
    );

    if (duplicate) {

        if (!adminWarnings[adminId]) {
            adminWarnings[adminId] = 0;
        }

        adminWarnings[adminId]++;

        if (adminWarnings[adminId] >= 3) {
            return res.json({
                message: "Duplicate record detected. Admin flagged!",
                adminFlagged: true
            });
        }

        return res.json({
            message: "Duplicate record detected",
            warnings: adminWarnings[adminId]
        });
    }

    records.push({ name, email, phone });

    res.json({
        message: "Record added successfully",
        data: records
    });
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});