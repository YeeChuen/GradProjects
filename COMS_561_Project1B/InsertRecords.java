/**
 * Author: Yee Chuen Teoh
 * Title: COM S 561 Project 1B
 * Reference: COM S Teachin staff, 
 * - Skeleton of the code acquire from previous project in COM S 363
 */
/**
 * assumption that project1B database has been created
 */
//package Project1B_JDBC;

import java.awt.Color;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.sql.Connection;
import java.sql.DriverManager;
//import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.border.LineBorder;

public class InsertRecords {
	
	public static String[] loginDialog() {

		// asking for a username and password to access the database.
		
		String result[] = new String[4];
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints cs = new GridBagConstraints();

		cs.fill = GridBagConstraints.HORIZONTAL;

		//get the username
		JLabel lbUsername = new JLabel("Username: ");
		cs.gridx = 0;
		cs.gridy = 0;
		cs.gridwidth = 1;
		panel.add(lbUsername, cs);
		JTextField tfUsername = new JTextField(20);
		cs.gridx = 1;
		cs.gridy = 0;
		cs.gridwidth = 2;
		panel.add(tfUsername, cs);
		
		//get the password
		JLabel lbPassword = new JLabel("Password: ");
		cs.gridx = 0;
		cs.gridy = 1;
		cs.gridwidth = 1;
		panel.add(lbPassword, cs);
		JPasswordField pfPassword = new JPasswordField(20);
		cs.gridx = 1;
		cs.gridy = 1;
		cs.gridwidth = 2;
		panel.add(pfPassword, cs);
		

		//get the server name user wanted to access
		JLabel lbServerName = new JLabel("Server name: ");
		cs.gridx = 0;
		cs.gridy = 2;
		cs.gridwidth = 1;
		panel.add(lbServerName, cs);
		JTextField tfServerName = new JTextField(20);
		cs.gridx = 1;
		cs.gridy = 2;
		cs.gridwidth = 2;
		panel.add(tfServerName, cs);
		
		//get the port number user wanted to access
		JLabel lbPortnum = new JLabel("Port number: ");
		cs.gridx = 0;
		cs.gridy = 3;
		cs.gridwidth = 1;
		panel.add(lbPortnum, cs);

		JTextField tfPortnum = new JTextField(20);
		cs.gridx = 1;
		cs.gridy = 3;
		cs.gridwidth = 2;
		panel.add(tfPortnum, cs);
		
		
		panel.setBorder(new LineBorder(Color.GRAY));

		String[] options = new String[] { "OK", "Cancel" };
		int ioption = JOptionPane.showOptionDialog(null, panel, "Login", JOptionPane.OK_OPTION,
				JOptionPane.PLAIN_MESSAGE, null, options, options[0]);
		
		// store the username in the first slot.
		// store the password in the second slot.
		// store the servername in the third slot.
		// store the port number in the fourth slot.
		
		if (ioption == 0) // pressing OK button
		{
			result[0] = tfUsername.getText();
			result[1] = new String(pfPassword.getPassword());
			result[2] = tfServerName.getText();
			result[3] = tfPortnum.getText();
		}
		return result;
	}
	
	/**
	 * updateSQL runs query "QueryTorun" in MySQL
	 * @param conn
	 * @param QueryTorun
	 */
	public static void updateSQL(Connection conn, String QueryTorun) {
		Statement stmt;
		try {
			stmt = conn.createStatement();
			stmt.executeUpdate(QueryTorun);
			stmt.close();
			System.out.println("Update success\n");
		} catch (SQLException e) {
			System.out.println("Update failed\n");
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {

		
		//login user 
		//String dbServer = "jdbc:mysql://127.0.0.1:3306/";
		String dbTest = "jdbc:mysql://";
		String userName = "";
		String password = "";
		String serverName = "";
		String portNum = "";

		String result[] = loginDialog();
//		userName = result[0];
//		password = result[1];
//		serverName = result[2];
//		portNum = result[3];
		userName = "Yee Chuen";
		password = "Krustykrab98*";
		serverName = "127.0.0.1";
		portNum = "3306";
		dbTest = dbTest + serverName + ":"+portNum+"/coms561project1b?allowPublicKeyRetrieval=true&useSSL=true";
		System.out.print("--- Connecting to " +dbTest + " ---\n");
		
		Connection conn=null;
		
		if (result[0]==null || result[1]==null) {
			System.out.println("Terminating: No username nor password is given");
			return;
		}
		try {
			// load JDBC driver
			// must be in the try-catch-block
			Class.forName("com.mysql.cj.jdbc.Driver");
			conn = DriverManager.getConnection(dbTest, userName, password);
			
			System.out.print("Connection secure \n");
			
			//run the queries here
			conn.setAutoCommit(false);
			/**
			 * full protection against interference from other transaction
			 * prevent dirty read
			 * prevent unrepeatable reads
			 * prevent phantom reads		
			 */
			conn.setTransactionIsolation(Connection.TRANSACTION_SERIALIZABLE );
			
			//make sure using the right database
			System.out.print("--- connecting to database coms561project1b ---\n");
			updateSQL(conn, "use coms561project1b;");
			
			//insert records to students table
			System.out.print("--- inserting record to students table ---\n");
			updateSQL(conn, "insert into students values\r\n"
					+ "(1001, 654651234, 'Randy', 'M', '2000-12-01', '301 E Hall', 5152700966, '121 Main', 7083066321),\r\n"
					+ "(1002, 123097834, 'Victor', 'M', '2000-05-06', '270 W Hall', 5151234578, '702 Walnut', 7080366333),\r\n"
					+ "(1003, 978012431, 'John', 'M', '1999-07-08', '201 W Hall', 5154132805, '888 University', 5152012011),\r\n"
					+ "(1004, 746897816, 'Seth', 'M', '1998-12-30', '199 N Hall', 5158891504, '21 Green', 5154132907),\r\n"
					+ "(1005, 186032894, 'Nicole', 'F', '2001-04-01', '178 S Hall', 5158891155, '13 Gray', 5157162071),\r\n"
					+ "(1006, 534218752, 'Becky', 'F', '2001-05-16', '12 N Hall', 5157083698, '189 Clark', 2034367632),\r\n"
					+ "(1007, 432609519, 'Kevin', 'M', '2000-08-12', '75 E Hall', 5157082497, '89 National', 7182340772);");
				

			//insert records to students table
			System.out.print("--- inserting record to departments table ---\n");
			updateSQL(conn, "insert into departments values\r\n"
					+ "(401, 'Computer Science', 5152982801, 'LAS'),\r\n"
					+ "(402, 'Mathematics', 5152982802, 'LAS'),\r\n"
					+ "(403, 'Chemical Engineering', 5152982803, 'Engineering'),\r\n"
					+ "(404, 'Landscape Architect', 5152982804, 'Design');\r\n"
					+ "");
			

			//insert records to students table
			System.out.print("--- inserting record to degrees table ---\n");
			updateSQL(conn, "insert into degrees values\r\n"
					+ "('Computer Science', 'BS', 401),\r\n"
					+ "('Software Engineering', 'BS', 401),\r\n"
					+ "('Computer Science', 'MS', 401),\r\n"
					+ "('Computer Science', 'PhD', 401),\r\n"
					+ "('Applied Mathematics', 'MS', 402),\r\n"
					+ "('Chemical Engineering', 'BS', 403),\r\n"
					+ "('Landscape Architect', 'BS', 404);");
			

			//insert records to students table
			System.out.print("--- inserting record to major table ---\n");
			updateSQL(conn, "insert into major values\r\n"
					+ "(1001, 'Computer Science', 'BS'),\r\n"
					+ "(1002, 'Software Engineering', 'BS'),\r\n"
					+ "(1003, 'Chemical Engineering', 'BS'),\r\n"
					+ "(1004, 'Landscape Architect', 'BS'),\r\n"
					+ "(1005, 'Computer Science', 'MS'),\r\n"
					+ "(1006, 'Applied Mathematics', 'MS'),\r\n"
					+ "(1007, 'Computer Science', 'PhD');");
			

			//insert records to students table
			System.out.print("--- inserting record to minor table ---\n");
			updateSQL(conn, "insert into minor values\r\n"
					+ "(1007, 'Applied Mathematics', 'MS'),\r\n"
					+ "(1005, 'Applied Mathematics', 'MS'),\r\n"
					+ "(1001, 'Software Engineering', 'BS');\r\n"
					+ "");
			

			//insert records to students table
			System.out.print("--- inserting record to courses table ---\n");
			updateSQL(conn, "insert into courses values\r\n"
					+ "(113, 'Spreadsheet', 'Microsoft Excel and Access', 3, 'Undergraduate', 401),\r\n"
					+ "(311, 'Algorithm', 'Design and Analysis', 3, 'Undergraduate', 401),\r\n"
					+ "(531, 'Theory of Computation', 'Theorem and Probability ', 3, 'Graduate', 401),\r\n"
					+ "(363, 'Database', 'Design Principle', 3, 'Undergraduate', 401),\r\n"
					+ "(412, 'Water Management', 'Water Management', 3, 'Undergraduate', 404),\r\n"
					+ "(228, 'Special Topics', 'Interesting Topics about CE', 3, 'Undergraduate', 403),\r\n"
					+ "(101, 'Calculus', 'Limit and Derivative', 4, 'Undergraduate', 402);\r\n"
					+ "");
			

			//insert records to students table
			System.out.print("--- inserting record to register table ---\n");
			updateSQL(conn, "insert into register values\r\n"
					+ "(1001, 363, 'Fall2020', 3),\r\n"
					+ "(1002, 311, 'Fall2020', 4),\r\n"
					+ "(1003, 228, 'Fall2020', 4),\r\n"
					+ "(1004, 363, 'Spring2021', 3),\r\n"
					+ "(1005, 531, 'Spring2021', 4),\r\n"
					+ "(1006, 363, 'Fall2020', 3),\r\n"
					+ "(1007, 531, 'Spring2021', 4);\r\n"
					+ "");
			
			
			//commit to updates
			conn.commit();
			conn.setAutoCommit(true);
			
		}
		 catch (Exception e) {
				
				System.out.println("Program terminates due to errors or user cancelation");
				e.printStackTrace(); // for debugging; 
		}
}
}
