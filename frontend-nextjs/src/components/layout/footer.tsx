export function Footer() {
  return (
    <footer className="bg-gray-800 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Restaurant Recommendations</h3>
            <p className="text-gray-300 text-sm">
              AI-powered restaurant recommendation system that helps you discover the perfect dining spots tailored to your preferences.
            </p>
          </div>
          
          <div>
            <h4 className="text-md font-medium mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">How it Works</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Terms of Service</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-md font-medium mb-4">Connect</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">GitHub</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Twitter</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">LinkedIn</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-8 text-center">
          <p className="text-gray-400 text-sm">
            © 2024 Restaurant Recommendations. Built with Next.js and FastAPI.
          </p>
        </div>
      </div>
    </footer>
  );
}
