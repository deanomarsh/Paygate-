// Mock database of unclaimed money records
const unclaimedMoneyDatabase = [
    {
        id: 1,
        firstName: "John",
        lastName: "Smith",
        city: "Los Angeles",
        state: "CA",
        amount: 1250.00,
        type: "Uncashed Paycheck",
        company: "ABC Corporation",
        year: 2019
    },
    {
        id: 2,
        firstName: "John",
        lastName: "Smith",
        city: "San Francisco",
        state: "CA",
        amount: 850.00,
        type: "Bank Account",
        company: "First National Bank",
        year: 2018
    },
    {
        id: 3,
        firstName: "Jane",
        lastName: "Doe",
        city: "New York",
        state: "NY",
        amount: 3500.00,
        type: "Insurance Refund",
        company: "Safety Insurance Co.",
        year: 2020
    },
    {
        id: 4,
        firstName: "Jane",
        lastName: "Doe",
        city: "Brooklyn",
        state: "NY",
        amount: 275.00,
        type: "Utility Deposit",
        company: "Power & Light Company",
        year: 2017
    },
    {
        id: 5,
        firstName: "Michael",
        lastName: "Johnson",
        city: "Chicago",
        state: "IL",
        amount: 5200.00,
        type: "Stock Dividends",
        company: "Investment Holdings LLC",
        year: 2019
    },
    {
        id: 6,
        firstName: "Sarah",
        lastName: "Williams",
        city: "Houston",
        state: "TX",
        amount: 420.00,
        type: "Tax Refund",
        company: "State Treasury",
        year: 2021
    },
    {
        id: 7,
        firstName: "Robert",
        lastName: "Brown",
        city: "Phoenix",
        state: "AZ",
        amount: 1850.00,
        type: "Security Deposit",
        company: "Phoenix Property Management",
        year: 2018
    },
    {
        id: 8,
        firstName: "Emily",
        lastName: "Davis",
        city: "Seattle",
        state: "WA",
        amount: 920.00,
        type: "Vendor Payment",
        company: "Tech Solutions Inc.",
        year: 2020
    },
    {
        id: 9,
        firstName: "David",
        lastName: "Miller",
        city: "Boston",
        state: "MA",
        amount: 2100.00,
        type: "Life Insurance Benefit",
        company: "Metropolitan Life",
        year: 2019
    },
    {
        id: 10,
        firstName: "Jennifer",
        lastName: "Wilson",
        city: "Miami",
        state: "FL",
        amount: 680.00,
        type: "Rebate",
        company: "Electronics Mart",
        year: 2021
    },
    {
        id: 11,
        firstName: "James",
        lastName: "Anderson",
        city: "Denver",
        state: "CO",
        amount: 1575.00,
        type: "Uncashed Paycheck",
        company: "Mountain Construction",
        year: 2018
    },
    {
        id: 12,
        firstName: "Mary",
        lastName: "Taylor",
        city: "Portland",
        state: "OR",
        amount: 3200.00,
        type: "Inheritance",
        company: "Estate of John Taylor",
        year: 2020
    }
];

// Search functionality
document.getElementById('searchForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form values
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const city = document.getElementById('city').value.trim();
    const state = document.getElementById('state').value;
    
    // Show loading spinner
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    // Simulate API delay
    setTimeout(() => {
        const results = searchDatabase(firstName, lastName, city, state);
        displayResults(results, firstName, lastName);
        
        // Hide loading spinner and show results
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'block';
        
        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }, 1500);
});

// Search database function
function searchDatabase(firstName, lastName, city, state) {
    return unclaimedMoneyDatabase.filter(record => {
        // Case-insensitive match for names
        const firstNameMatch = record.firstName.toLowerCase() === firstName.toLowerCase();
        const lastNameMatch = record.lastName.toLowerCase() === lastName.toLowerCase();
        
        // Optional city and state filters
        const cityMatch = !city || record.city.toLowerCase().includes(city.toLowerCase());
        const stateMatch = !state || record.state === state;
        
        return firstNameMatch && lastNameMatch && cityMatch && stateMatch;
    });
}

// Display results function
function displayResults(results, firstName, lastName) {
    const resultsContainer = document.getElementById('resultsContainer');
    
    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="no-results">
                <h3>No matches found for ${firstName} ${lastName}</h3>
                <p>We couldn't find any unclaimed money records matching your search.</p>
                <p><strong>What you can do:</strong></p>
                <ul>
                    <li>Try searching with different variations of your name</li>
                    <li>Search without city or state filters for broader results</li>
                    <li>Check if you've used previous addresses or maiden names</li>
                    <li>Search for family members who may have listed you as beneficiary</li>
                    <li>Try again later - our database is updated regularly</li>
                </ul>
            </div>
        `;
        return;
    }
    
    const totalAmount = results.reduce((sum, record) => sum + record.amount, 0);
    
    let html = `
        <div style="background-color: #d4edda; border: 2px solid #28a745; border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem;">
            <h3 style="color: #155724; margin-bottom: 0.5rem;">🎉 Great News!</h3>
            <p style="color: #155724; font-size: 1.1rem;">We found <strong>${results.length}</strong> record${results.length > 1 ? 's' : ''} with a total value of <strong>$${totalAmount.toFixed(2)}</strong></p>
        </div>
    `;
    
    results.forEach(record => {
        html += `
            <div class="result-card">
                <h3>💰 $${record.amount.toFixed(2)}</h3>
                <div class="result-details">
                    <div class="result-detail">
                        <strong>Type:</strong>
                        <span>${record.type}</span>
                    </div>
                    <div class="result-detail">
                        <strong>Source:</strong>
                        <span>${record.company}</span>
                    </div>
                    <div class="result-detail">
                        <strong>Location:</strong>
                        <span>${record.city}, ${record.state}</span>
                    </div>
                    <div class="result-detail">
                        <strong>Year:</strong>
                        <span>${record.year}</span>
                    </div>
                </div>
                <button class="claim-button" onclick="showClaimInstructions(${record.id})">
                    How to Claim This Money
                </button>
            </div>
        `;
    });
    
    resultsContainer.innerHTML = html;
}

// Show claim instructions
function showClaimInstructions(recordId) {
    const record = unclaimedMoneyDatabase.find(r => r.id === recordId);
    
    const instructionsHTML = `
        <div style="background-color: #f8f9fa; border-left: 4px solid #667eea; padding: 1.5rem; margin-top: 1rem; border-radius: 4px;">
            <h4 style="color: #667eea; margin-bottom: 1rem;">How to Claim This Money</h4>
            <ol style="margin-left: 1.5rem; line-height: 1.8;">
                <li>Contact the <strong>${record.company}</strong> directly</li>
                <li>Provide proof of identity (driver's license, passport)</li>
                <li>Provide proof of address (utility bill, bank statement)</li>
                <li>Complete the state's unclaimed property claim form</li>
                <li>Submit your claim to your state's unclaimed property office</li>
            </ol>
            <p style="margin-top: 1rem;"><strong>For ${record.state}:</strong> Visit your state treasury website or call their unclaimed property division.</p>
            <p style="background-color: #d4edda; padding: 0.75rem; border-radius: 4px; margin-top: 1rem; color: #155724;"><strong>⚠️ Important:</strong> This is a FREE service - never pay anyone to help you claim your money!</p>
        </div>
    `;
    
    // Find the button that was clicked and insert instructions after its parent card
    const button = event.target;
    const card = button.closest('.result-card');
    
    // Check if instructions are already shown
    const existingInstructions = card.querySelector('.claim-instructions');
    if (existingInstructions) {
        existingInstructions.remove();
        button.textContent = 'How to Claim This Money';
    } else {
        const instructionsDiv = document.createElement('div');
        instructionsDiv.className = 'claim-instructions';
        instructionsDiv.innerHTML = instructionsHTML;
        card.appendChild(instructionsDiv);
        button.textContent = 'Hide Instructions';
    }
}

// Form validation
document.getElementById('zipCode').addEventListener('input', function(e) {
    const value = e.target.value;
    // Filter out non-numeric characters and limit to 5 digits
    const numericValue = value.replace(/\D/g, '').slice(0, 5);
    if (value !== numericValue) {
        e.target.value = numericValue;
    }
});

// Add smooth scrolling for all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Initialize page
console.log('Unclaimed Money Finder initialized');
console.log(`Database contains ${unclaimedMoneyDatabase.length} records`);
