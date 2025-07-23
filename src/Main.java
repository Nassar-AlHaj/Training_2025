
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Library library = new Library();
        Scanner input = new Scanner(System.in);
        int choice;

        do {
            System.out.println("\n=== Library Menu ===");
            System.out.println("1. Add Book");
            System.out.println("2. Show All Books");
            System.out.println("3. Search Book by Title");
            System.out.println("4. Delete Book by ID");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");
            choice = input.nextInt();
            input.nextLine();

            switch (choice) {
                case 1:
                    System.out.print("Enter Book ID: ");
                    int id = input.nextInt();
                    input.nextLine();

                    if (library.isIdExists(id)) {
                        System.out.println("❌ ID already exists! Please choose a different ID.");
                        break;
                    }

                    System.out.print("Enter Book Title: ");
                    String title = input.nextLine();

                    System.out.print("Enter Book Author: ");
                    String author = input.nextLine();

                    System.out.print("Enter Book Year: ");
                    int year = input.nextInt();

                    Book newBook = new Book(id, title, author, year);
                    library.addBook(newBook);
                    break;

                case 2:
                    library.displayBooks();
                    break;

                case 3:
                    System.out.print("Enter title to search: ");
                    String searchTitle = input.nextLine();
                    library.searchBookByTitle(searchTitle);
                    break;

                case 4:
                    System.out.print("Enter ID to delete: ");
                    int deleteId = input.nextInt();
                    library.deleteBookById(deleteId);
                    break;

                case 5:
                    System.out.println("Exiting the program.");
                    break;

                default:
                    System.out.println("Invalid choice. Please try again.");
            }

        } while (choice != 5);

        input.close();
    }
}
