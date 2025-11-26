import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import path from 'path';

// تحميل environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// خدمة الملفات الثابتة
app.use('/css', express.static(path.join(__dirname, 'public/css')));
app.use('/js', express.static(path.join(__dirname, 'public/js')));
app.use('/images', express.static(path.join(__dirname, 'public/images')));

// إعداد view engine مع EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '../views'));

// Route الأساسية للتحقق
app.get('/api/health', (req, res) => {
  res.status(200).json({
    status: 'success',
    message: '🚀 Server is running successfully!',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development'
  });
});

// Route للصفحة الرئيسية - الإصدار المصحح
app.get('/', (req, res) => {
  res.render('home', {
    title: 'الرئيسية',
    body: 'home'
  });
});

// Route تجريبي للتحقق من أن الـ views تعمل
app.get('/test', (req, res) => {
  res.render('layout', {
    title: 'صفحة اختبار',
    body: '<h1>هذه صفحة اختبار</h1><p>الـ views تعمل بشكل صحيح الآن!</p>'
  });
});

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error(err.stack);
  res.status(500).render('error', {
    title: 'خطأ',
    message: 'حدث خطأ في الخادم!'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).render('error', {
    title: 'غير موجود',
    message: 'الصفحة التي تبحث عنها غير موجودة'
  });
});

app.listen(PORT, () => {
  console.log(`🛍️ Ecommerce server is running on port ${PORT}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/api/health`);
  console.log(`🏠 Home page: http://localhost:${PORT}`);
  console.log(`🧪 Test page: http://localhost:${PORT}/test`);
});

export default app;
