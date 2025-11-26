# 🛍️ متجر إلكتروني - Ecommerce Project

مشروع متجر إلكتروني متكامل مبني باستخدام:

## 🚀 المكدس التقني
- **Backend:** Node.js + Express.js + TypeScript
- **Database:** PostgreSQL + Prisma ORM
- **Authentication:** JWT + bcryptjs
- **Validation:** Zod
- **Security:** Helmet + CORS
- **Logging:** Morgan

## 📦 التبعيات المثبتة
```bash
npm install

cat > src/index.ts << 'EOF'
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';

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

// Route الأساسية للتحقق
app.get('/api/health', (req, res) => {
res.status(200).json({
status: 'success',
message: '🚀 Server is running successfully!',
timestamp: new Date().toISOString(),
environment: process.env.NODE_ENV || 'development'
});
});

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
console.error(err.stack);
res.status(500).json({
status: 'error',
message: 'Something went wrong!'
});
});

// 404 handler
app.use('*', (req, res) => {
res.status(404).json({
status: 'error',
message: 'Route not found'
});
});

app.listen(PORT, () => {
console.log(🛍️ Ecommerce server is running on port ${PORT});
console.log(🔗 Health check: http://localhost:${PORT}/api/health);
});

export default app;
