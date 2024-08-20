import time
import threading

class User:
    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role = role

class Auction:
    def __init__(self, auction_id, item_name, description, starting_price, duration_minutes):
        self.auction_id = auction_id
        self.item_name = item_name
        self.description = description
        self.starting_price = starting_price
        self.current_price = starting_price
        self.duration_minutes = duration_minutes
        self.bids = []
        self.is_active = True
        self.highest_bidder = None
        self.end_time = time.time() + duration_minutes * 60

    def place_bid(self, user, bid_amount):
        if not self.is_active:
            return "Auction has ended."
        if bid_amount <= self.current_price:
            return f"Bid must be higher than the current price of {self.current_price}."

        self.current_price = bid_amount
        self.highest_bidder = user
        self.bids.append((user, bid_amount))
        return "Bid placed successfully!"

    def check_auction_status(self):
        if time.time() >= self.end_time:
            self.is_active = False
            return self.declare_winner()
        return "Auction is still ongoing."

    def declare_winner(self):
        if self.highest_bidder:
            return f"Auction ended! Winner is {self.highest_bidder.name} with a bid of ₹'{self.current_price}."
        else:
            return "Auction ended with no bids."

class AuctionSystem:
    def __init__(self):
        self.users = {}
        self.auctions = {}
        self.auction_counter = 1
        self.user_counter = 1

    def register_user(self, name, role):
        user_id = self.user_counter
        user = User(user_id, name, role)
        self.users[user_id] = user
        self.user_counter += 1
        return user

    def create_auction(self, auctioneer, item_name, description, starting_price, duration_minutes):
        if auctioneer.role != 'auctioneer':
            return "Only auctioneers can create auctions."

        auction_id = self.auction_counter
        auction = Auction(auction_id, item_name, description, starting_price, duration_minutes)
        self.auctions[auction_id] = auction
        self.auction_counter += 1

        # Start a background thread to monitor the auction end time
        threading.Thread(target=self.monitor_auction, args=(auction,)).start()

        return f"Auction created successfully with ID: {auction_id}"

    def view_auctions(self):
        if not self.auctions:
            return "No ongoing auctions at the moment."

        auction_list = []
        for auction in self.auctions.values():
            status = "Active" if auction.is_active else "Ended"
            auction_list.append(f"Auction ID: {auction.auction_id}, Item: {auction.item_name}, Current Price: ₹{auction.current_price}, Status: {status}")

        return "\n".join(auction_list)

    def place_bid(self, bidder, auction_id, bid_amount):
        if bidder.role != 'bidder':
            return "Only bidders can place bids."

        auction = self.auctions.get(auction_id)
        if not auction:
            return "Invalid auction ID."

        return auction.place_bid(bidder, bid_amount)

    def view_auction_results(self, auction_id):
        auction = self.auctions.get(auction_id)
        if not auction:
            return "Invalid auction ID."
        return auction.check_auction_status()

    def monitor_auction(self, auction):
        while auction.is_active:
            if time.time() >= auction.end_time:
                auction.is_active = False
        print(auction.declare_winner())

def main():
    system = AuctionSystem()

    while True:
        print("\nWelcome to the Online Auction System")
        print("1. Register as a User")
        print("2. Login")
        print("3. Create Auction (Auctioneer)")
        print("4. View Ongoing Auctions (Bidder)")
        print("5. Place a Bid (Bidder)")
        print("6. View Auction Results")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            role = input("Enter role (auctioneer/bidder): ").lower()
            if role not in ['auctioneer', 'bidder']:
                print("Invalid role! Please choose 'auctioneer' or 'bidder'.")
                continue
            user = system.register_user(name, role)
            print(f"User registered successfully! User ID: {user.user_id}, Name: {user.name}, Role: {user.role}")

        elif choice == '2':
            user_id = int(input("Enter your user ID: "))
            user = system.users.get(user_id)
            if not user:
                print("Invalid user ID!")
            else:
                print(f"Logged in as {user.name} ({user.role})")

        elif choice == '3':
            if not user or user.role != 'auctioneer':
                print("Only auctioneers can create auctions.")
                continue
            item_name = input("Enter item name: ")
            description = input("Enter item description: ")
            starting_price = float(input("Enter starting price: ₹ "))
            duration_minutes = int(input("Enter auction duration (in minutes): "))
            result = system.create_auction(user, item_name, description, starting_price, duration_minutes)
            print(result)

        elif choice == '4':
            print(system.view_auctions())

        elif choice == '5':
            if not user or user.role != 'bidder':
                print("Only bidders can place bids.")
                continue
            auction_id = int(input("Enter Auction ID to place a bid: "))
            bid_amount = float(input("Enter your bid amount: ₹ "))
            result = system.place_bid(user, auction_id, bid_amount)
            print(result)

        elif choice == '6':
            auction_id = int(input("Enter Auction ID to view results: "))
            result = system.view_auction_results(auction_id)
            print(result)

        elif choice == '7':
            print("Exiting the system. Thank you!")
            break

        else:
            print("Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    main()
