// Main JavaScript for ETH Investment Dashboard

// Firebase configuration
const firebaseConfig = {
  // This will be replaced with actual Firebase config during deployment
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

// Authentication state observer
auth.onAuthStateChanged(function(user) {
  if (user) {
    // User is signed in
    user.getIdToken().then(function(idToken) {
      // Send token to server
      fetch('/sessionLogin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({idToken: idToken}),
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          console.log('User authenticated with server');
          // If on login page, redirect to dashboard
          if (window.location.pathname === '/login') {
            window.location.href = '/';
          }
        } else {
          console.error('Error authenticating with server:', data.error);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
  } else {
    // User is signed out
    console.log('User is signed out');
    // If not on login page, redirect to login
    if (window.location.pathname !== '/login') {
      window.location.href = '/login';
    }
  }
});

// Google Sign-In
function signInWithGoogle() {
  const provider = new firebase.auth.GoogleAuthProvider();
  auth.signInWithPopup(provider)
    .catch(error => {
      console.error('Error signing in with Google:', error);
      document.getElementById('error-message').textContent = error.message;
    });
}

// Sign out
function signOut() {
  auth.signOut()
    .then(() => {
      console.log('User signed out');
      window.location.href = '/login';
    })
    .catch(error => {
      console.error('Error signing out:', error);
    });
}

// Show loading spinner
function showLoading(message = 'Loading...') {
  const spinner = document.createElement('div');
  spinner.className = 'spinner-overlay';
  spinner.innerHTML = `
    <div class="spinner-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">${message}</p>
    </div>
  `;
  document.body.appendChild(spinner);
}

// Hide loading spinner
function hideLoading() {
  const spinner = document.querySelector('.spinner-overlay');
  if (spinner) {
    spinner.remove();
  }
}

// Format currency
function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(value);
}

// Format percentage
function formatPercentage(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value / 100);
}

// Toggle dark mode
function toggleDarkMode() {
  document.body.classList.toggle('dark-mode');
  const isDarkMode = document.body.classList.contains('dark-mode');
  localStorage.setItem('darkMode', isDarkMode);
}

// Initialize dark mode from localStorage
document.addEventListener('DOMContentLoaded', function() {
  const isDarkMode = localStorage.getItem('darkMode') === 'true';
  if (isDarkMode) {
    document.body.classList.add('dark-mode');
  }
  
  // Initialize tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});
