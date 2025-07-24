import java.util.ArrayList;
import java.io.*;

public class Library {
    private ArrayList<Book> books = new ArrayList<>();

    public void addBook(Book book) {
        books.add(book);
        System.out.println("Book added successfully.");
    }

    public void displayBooks() {
        if (books.isEmpty()) {
            System.out.println("No books in the library.");
        } else {
            for (Book book : books) {
                System.out.println(book);
            }
        }
    }

    public void searchBookByTitle(String title) {
        boolean found = false;
        for (Book book : books) {
            if (book.getTitle().equalsIgnoreCase(title)) {
                System.out.println(book);
                found = true;
            }
        }
        if (!found) {
            System.out.println("No book found with the title: " + title);
        }
    }

    public void deleteBookById(int id) {
        Book toRemove = null;
        for (Book book : books) {
            if (book.getId() == id) {
                toRemove = book;
                break;
            }
        }
        if (toRemove != null) {
            books.remove(toRemove);
            System.out.println("Book deleted successfully.");
        } else {
            System.out.println("No book found with ID: " + id);
        }
    }
    public boolean isIdExists(int id) {
        for (Book book : books) {
            if (book.getId() == id) {
                return true;
            }
        }
        return false;
    }


    public void loadBooksFromFile(String filename) {
        books.clear();
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 4) {
                    int id = Integer.parseInt(parts[0]);
                    String title = parts[1];
                    String author = parts[2];
                    int year = Integer.parseInt(parts[3]);
                    books.add(new Book(id, title, author, year));
                }
            }
        } catch (IOException e) {
            System.out.println("⚠️ File not found. Starting with an empty library.");
        }
    }
    public void saveBooksToFile(String filename) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(filename))) {
            for (Book book : books) {
                writer.println(book.getId() + "," + book.getTitle() + "," +
                        book.getAuthor() + "," + book.getYear());
            }
        } catch (IOException e) {
            System.out.println("❌ Error saving books: " + e.getMessage());
        }
    }

}
