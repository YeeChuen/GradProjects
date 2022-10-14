/**
 * Author: Yee Chuen Teoh
 * Title: COM S 561 Project 1B
 * Reference: COM S Teachin staff, 
 * - Skeleton of the code acquire from previous project in COM S 363
 */
//package Project1B_JDBC;

import java.awt.Color;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.border.LineBorder;

public class DropTables {
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
			
			updateSQL(conn, "Set FOREIGN_KEY_CHECKS=0;");
			updateSQL(conn, "drop table students;");
			updateSQL(conn, "drop table departments;");
			updateSQL(conn, "drop table courses;");
			updateSQL(conn, "drop table degrees;");
			updateSQL(conn, "drop table register;");
			updateSQL(conn, "drop table major;");
			updateSQL(conn, "drop table minor;");
			updateSQL(conn, "Set FOREIGN_KEY_CHECKS=1;");
			
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
