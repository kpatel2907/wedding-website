# Wedding Website 💍

A beautiful, elegant wedding website featuring multiple pages for your special celebration.

## Features

- **Welcome Page** - A stunning hero section with the couple's names and wedding date
- **Our Story Page** - A timeline of the couple's journey together
- **Events Page** - Details of all 4 wedding events:
  - Mendhi
  - Vidhi
  - Wedding
  - Reception
- **RSVP Page** - A form for guests to RSVP to the events

## Getting Started

### Option 1: Open directly in browser
Simply double-click the `index.html` file or open it in any web browser.

### Option 2: Use a local server (recommended for development)
Using Python:
```bash
cd wedding-website
python -m http.server 8000
```
Then open http://localhost:8000 in your browser.

Using Node.js (with http-server):
```bash
npx http-server
```

## Customization

### Update Names and Dates
Edit `index.html` and update:
- Couple's names in the hero section
- Wedding date and location
- Event dates, times, and venues
- Our Story timeline content

### Update Colors
Edit `styles.css` and modify the CSS variables at the top:
```css
:root {
    --color-primary: #b8860b;      /* Gold - main accent color */
    --color-secondary: #f5e6d3;    /* Light beige */
    --color-text: #2c2c2c;         /* Dark text */
    /* ... more colors */
}
```

### Add Photos
Create an `images` folder and add your photos. Then update the HTML to include them:
```html
<img src="images/your-photo.jpg" alt="Description">
```

## File Structure

```
wedding-website/
├── index.html      # Main HTML file with all pages
├── styles.css      # All styling
├── script.js       # Navigation and form handling
└── README.md       # This file
```

## Browser Support

Works on all modern browsers:
- Chrome
- Firefox
- Safari
- Edge

## License

Free to use for your wedding! 🎉
