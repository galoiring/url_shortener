# 🔗 URL Shortener

> A simple and efficient URL shortener built with Django and Tailwind CSS. This application allows users to create shortened URLs, manage their URL history, and easily copy shortened links to their clipboard.

<p align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind"/>
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
</p>

## ✨ Features

- 🔄 Shorten any valid URL
- 📋 Copy shortened URLs to clipboard with one click
- 📜 View history of recently shortened URLs
- 🗑️ Delete URLs from history
- 📱 Responsive design that works on desktop and mobile
- 💾 Local storage for URL history
- ⌨️ Enter key support for quick URL shortening

## 🛠️ Tech Stack

- **Backend:** Django
- **Frontend:** HTML, JavaScript
- **CSS Framework:** Tailwind CSS
- **Database:** SQLite

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/url-shortener.git
   cd url-shortener
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## 📝 Usage

1. Navigate to `http://localhost:8000` in your web browser
2. Enter a long URL in the input field
3. Click "Shorten URL" or press Enter
4. Copy the shortened URL to your clipboard by clicking the copy button
5. View your URL history below the input field

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to Django for the amazing web framework
- Tailwind CSS for the styling utilities
- All contributors who help improve this project

## 📸 Screenshots

<div align="center">
  <figure>
    <img src="docs/images/Screenshot 1.png" alt="URL Shortener Interface" width="800"/>
    <figcaption>URL Shortener - Main Interface</figcaption>
  </figure>
</div>

## 🔮 Future Improvements

- [ ] User authentication system
- [ ] Custom URL slugs
- [ ] Analytics dashboard
- [ ] API endpoints
- [ ] QR code generation

## 📞 Support

If you have any questions or need help, please open an issue or contact the maintainers.

---

<p align="center">
  Made with ❤️ by [Your Name]
</p>
