const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const authRoutes = require('./routes/auth');

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const MONGO_URI = process.env.MONGO_URI || 'mongodb+srv://kalyankumarmuli64_db_user:KkA%4019012005@cluster0.lwbvdka.mongodb.net/';
const PORT = process.env.PORT || 4000;

mongoose.connect(MONGO_URI, { connectTimeoutMS: 10000 })
  .then(() => console.log('Connected to MongoDB'))
  .catch((err) => console.error('MongoDB connection error:', err.message));

app.use('/api/auth', authRoutes);

app.get('/', (_, res) => res.json({ ok: true, msg: 'Backend running' }));

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
