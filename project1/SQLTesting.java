import java.sql.*;
import java.util.Scanner;
import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

class Answer {
	int numColumns = -1;
	ArrayList<String[]> values = new ArrayList<String[]>();

	void setNumColumns(int n) { numColumns = n; }
	int getNumColumns() { return numColumns; }
	int getNumRows() { return values.size(); }

	String get(int i, int j) { return values.get(i)[j]; }

	void print() {
		for(int row = 0; row < values.size(); row++)  {
			for(int col = 0; col < values.get(row).length; col++) 
				System.out.print(values.get(row)[col] + " ### ");
			System.out.println();
		}
	}

	HashMap<String, Integer> toHashMap() {
		HashMap<String, Integer> hm = new HashMap<String, Integer>();
		for(int i = 0; i < getNumRows(); i++) {
			for(int j = 0; j < getNumColumns(); j++) {
				String t = get(i,j).trim();
				Integer ii = hm.get(t);
				hm.put(t, ii == null ? 1 : ii + 1);
			}
		}
		return hm;
	}
}

public class SQLTesting 
{
	// Read the correct answers from the answers file
	public static Answer[] readAnswers(String fileName) {
		Answer[] answers = new Answer[11];
		try {
			Scanner s = new Scanner(new File(fileName)).useDelimiter("\\s*====\\s*");
			while(s.hasNext()) {
				int queryNumber = s.nextInt();
				answers[queryNumber] = new Answer();
				Scanner ss = new Scanner(s.next());
				while(ss.hasNext()) 
					answers[queryNumber].values.add(ss.nextLine().split(" ### "));
				answers[queryNumber].setNumColumns(answers[queryNumber].values.get(0).length); // we are not going to have empty answers
			}
		} catch (Exception e ) {
			System.out.println(e);
		}
		return answers;
	}

	// Read the submitted queries
	public static String[] readQueries(String fileName) {
		String[] queries = new String[11];
		try {
			Scanner s = new Scanner(new File(fileName)).useDelimiter("\\s*====\\s*");
			while(s.hasNext())
				queries[s.nextInt()] = s.next();
		} catch (Exception e ) {
			System.out.println(e);
		}
		return queries;
	}

	static boolean match(String s1, String s2) {
		try {
			double d1 = Double.parseDouble(s1);
			double d2 = Double.parseDouble(s2);
			// If both are Numbers, are they close enough?
			return (Math.abs(d1 - d2)*100) < Math.abs(d1 + d2);
		} catch (Exception e) {
		}

		return s1.trim().equals(s2.trim());
	}

	static double computeJaccard(HashMap<String, Integer> hm1, HashMap<String, Integer> hm2, int total_size) {
		int intersection = 0;
		for(String t: hm1.keySet()) {
			if(hm2.get(t) != null)
				intersection += (hm1.get(t) <= hm2.get(t)) ? hm1.get(t) : hm2.get(t);
		}
		return intersection * 1.0 / (total_size - intersection);
	}

	static int compareAnswers(Answer test, Answer correct) {
		boolean sameNumberOfColumns = (test.getNumColumns() == correct.getNumColumns());
		boolean sameNumberOfRows = (test.getNumRows() == correct.getNumRows());

		if(!sameNumberOfColumns) {
			System.out.println("------ Incorrect number of columns in the answer. Score = 0");
			return 0;
		}
		// We may give partial credit if the number of rows is incorrect, but no partial answers if the number of columns is incorrect


		if(sameNumberOfRows) {
			// check for near-exact match
			int matches = 0, mismatches = 0;
			for(int i = 0; i < correct.getNumRows(); i++)  {
				for(int j = 0; j < correct.getNumColumns(); j++)  {
                    // System.out.println(correct.get(i,j) + " " + test.get(i, j) + " " + match(correct.get(i, j), test.get(i, j)));
					if(match(correct.get(i, j), test.get(i, j)))  
						matches++;
					else mismatches++;
				}
			}
			if(mismatches == 0) {
				System.out.println("------ Perfect match. Score = 4");
				return 4;
			} 
		} 

		// Compare the answers as a set of values
		HashMap<String, Integer> hm1 = correct.toHashMap();
		HashMap<String, Integer> hm2 = test.toHashMap();
		int total_size = correct.getNumRows()*correct.getNumColumns() + test.getNumRows()*test.getNumColumns();
		double jaccard = computeJaccard(hm1, hm2, total_size);

		if(jaccard > 0.9) {
			if(sameNumberOfRows) {
				System.out.println("------ Very similar, but not exact match. Score = 3");
				return 3;
			} else {
				System.out.println("------ Very similar answers, but incorrect number of rows. Score = 2");
				return 2;
			}
		}
		if(jaccard > 0.5) {
			System.out.println("------ Somewhat similar answers. Score = 1");
			return 1;
		} else {
			System.out.println("------ Answers too different. Score = 0");
			return 0;
		}
	}

	public static int testQuery(Connection connection, String query, Answer correctAnswer) {
		if(query == null) {
			System.out.println("------- No Answer. Score = 0.");
			return 0;
		} else {
			try {
				Statement stmt = null;
				stmt = connection.createStatement();
				System.out.println("Trying to execute query:\n" + query);
				Answer ans = new Answer();
				ResultSet rs = stmt.executeQuery(query);
				int numColumns = rs.getMetaData().getColumnCount();
				ans.setNumColumns(numColumns);
				while (rs.next()) {
					String[] arr = new String[numColumns];
					for(int i = 0; i < numColumns; i++) 
						arr[i] = rs.getString(i+1);
					ans.values.add(arr);
				}
				stmt.close();
				System.out.println("---------- Returned Answer ---------"); ans.print();
				System.out.println("---------- Comparing to Correct Answer ---------"); correctAnswer.print();
				int score = compareAnswers(ans, correctAnswer);
				return score;
			} catch (SQLException e ) {
				System.out.println(e);
				System.out.println("------- Error while executing the query. Score = 0.");
				return 0;
			}
		}
	}

	public static void main(String[] argv) {
		Options options = new Options();
		options.addOption("h", false, "print help");
		options.addOption("a", true, "file containing correct answers (default: queries.txt)");
		options.addOption("q", true, "file containing SQL queries (default: answers.txt)");
		options.addOption("p", true, "database port to use (default: 5432)");
		options.addOption("u", true, "database user name (default: terrapin)");
		options.addOption("w", true, "database user password (default: terrapin)");
		options.addOption("n", true, "query number to test (if not specified, all queries would be tested)");
		options.addOption("d", true, "database name to use (default: social)");
		options.addOption("i", false, "run in interactive fashion, stopping after each query");

		CommandLineParser parser = new DefaultParser();
		CommandLine cmd = null;
		try {
			cmd = parser.parse(options, argv);
		} catch (Exception e) {
			System.out.println("Failed to parse comand line properties: " + e);
			(new HelpFormatter()).printHelp("Main", options);
			System.exit(0);
		}


		if (cmd.hasOption("h")) {
			(new HelpFormatter()).printHelp("Main", options);
			System.exit(0);
		}

        boolean interactive = false;
        Scanner in_scanner = null;
        if(cmd.hasOption("i")) {
            interactive = true;
            in_scanner = new Scanner(System.in);
        }

		int port = Integer.parseInt(cmd.getOptionValue("p", "5432"));
		String databaseName = cmd.getOptionValue("d", "social");
		String user = cmd.getOptionValue("u", "terrapin");
		String password = cmd.getOptionValue("w", "terrapin");
		String answersFile = cmd.getOptionValue("a", "answers.txt");
		String queriesFile = cmd.getOptionValue("q", "queries.txt");

		Connection connection = getConnection(port, databaseName, user, password);

		Answer[] correctAnswers = readAnswers(answersFile);
		String[] queries = readQueries(queriesFile);

		if(cmd.hasOption("n")) {
			int queryNumber = Integer.parseInt(cmd.getOptionValue("n"));
			System.out.println("================================ Testing Question " + queryNumber + " ===================================================");
			testQuery(connection, queries[queryNumber], correctAnswers[queryNumber]);
		} else {
			int total = 0;
			for(int i = 1; i < queries.length; i++) {
				System.out.println("================================ Question " + i + " ===================================================");
				total += testQuery(connection, queries[i], correctAnswers[i]);
                if(interactive) {
                    System.out.println("\n\nPress Enter to Continue\n\n\n");
                    in_scanner.nextLine();
                }
			}
			System.out.println("Final Score (out of 40) = " + total);
		}
	}

	static Connection getConnection(int port, String dbName, String username, String password) {
		Connection connection = null;

		try {
			Class.forName("org.postgresql.Driver");
		} catch (ClassNotFoundException e) {
			System.out.println("Where is your PostgreSQL JDBC Driver? " + "Include in your library path!");
			e.printStackTrace();
			System.exit(1);
		}

		System.out.println("PostgreSQL JDBC Driver Registered!");

		try {
			String url = "jdbc:postgresql://localhost:" + port + "/" + dbName;
			connection = DriverManager.getConnection(url, username, password);
		} catch (SQLException e) {
			System.out.println("Connection Failed! Check output console");
			e.printStackTrace();
			System.exit(1);
		}

		if (connection == null) {
			System.out.println("Failed to make connection!");
			System.exit(1);
		}

		return connection;
	}

}
