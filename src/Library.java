import java.util.ArrayList;

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

}
