# Receipt_Processor
The Receipt Processor is a webservice that fulfils the documented API, it is to process and analyze receipt data. It leverages Docker for containerization, ensuring a consistent and isolated environment for execution.

## Prerequisites
Docker: Install Docker to run the application within a container.
Build the Docker Image:

    docker build -t receipt_processor .
    
Run the Docker Container:

    docker run --rm receipt_processor

## Project Structure
main.py: The main script to run the application. 

requirements.txt: Lists the Python dependencies.  

Dockerfile: Contains instructions to build the Docker image.

## The Problem

We want you to build a simple **receipt processor** which takes in JSON receipts, computes points based on certain rules, and allows the user to retrieve the computed points later. The challenge involves creating a RESTful API that can:

1. **Process a receipt** and return a unique ID for that receipt.
2. **Return the number of points** awarded for a previously processed receipt when asked.

Points are awarded based on the following rules:

1. **One point for every alphanumeric character in the retailer name.**
   - For example, `"Target"` has 6 alphanumeric characters.
2. **50 points if the total is a round dollar amount with no cents.**
   - For example, `3.00` or `12.00`.
3. **25 points if the total is a multiple of 0.25.**
   - For example, `3.00` or `12.50`.
4. **5 points for every two items on the receipt.**
   - For example, 2 items = 5 points; 4 items = 10 points, etc.
5. **If the trimmed length of the item description is a multiple of 3, multiply the price of the item by 0.2 and round up to the nearest integer. Sum all those points for all such items.**
   - For example, if an item’s description has 6 characters and its price is 2.50, then `2.50 * 0.2 = 0.50` which rounds up to `1` point for that item.
6. **6 points if the day in the purchase date is odd.**
7. **10 points if the purchase time is between 2:00pm and 4:00pm.**
   - We can assume the time is in 24-hour format (i.e. 14:00 to 15:59 would match this rule).

### Example

A receipt has the following attributes:
- **Retailer**: `Target`
  - Alphanumeric characters = 6 → 6 points
- **Total**: `10.00`
  - Round dollar amount = 50 points
  - Multiple of 0.25 = 25 points
- **Items**: 2 items total → 5 points (for every 2 items)
  - If one item has a 6 character description and costs 2.50:
    - 6 is a multiple of 3 → `2.50 * 0.2 = 0.50` → round up to `1` point
- **Purchase date**: 2022-01-02 (day = 2, which is even) → 0 points
- **Purchase time**: 13:01 (between 14:00 and 15:59? no) → 0 points

Summing the above:
- Retailer points: 6  
- Total-based points: 50 + 25 = 75  
- Items-based points: 5 (for 2 items) + 1 (for the special description) = 6  
- Date-based points: 0  
- Time-based points: 0  

**Total Points = 6 + 75 + 6 = 87**

## The API

You need to expose two endpoints:

1. `POST /receipts/process`
   - Expects a JSON object representing the receipt.
   - Returns a JSON object with an identifier for the receipt.
   
2. `GET /receipts/{id}/points`
   - Returns a JSON object containing the number of points awarded for that receipt.

### Example Flow

1. **POST /receipts/process** with a JSON body for a receipt.
   ```json
   {
     "retailer": "Target",
     "purchaseDate": "2022-01-02",
     "purchaseTime": "13:01",
     "items": [
       {
         "shortDescription": "Mountain Dew 12PK",
         "price": "6.49"
       },
       {
         "shortDescription": "Emils Cheese Pizza",
         "price": "12.25"
       }
     ],
     "total": "10.00"
   }
   
