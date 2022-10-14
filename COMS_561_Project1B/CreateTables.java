/**
 * Author: Yee Chuen Teoh
 * Title: COM S 561 Project 1B
 * Reference: COM S Teachin staff, 
 * - Skeleton of the code acquire from previous project in COM S 363
 */
/**
 * NOTES:
 *  - Line 143-150 to be edited again (username, password, servername, portnum)
 */

//package Project1B_JDBC;

import java.sql.*;
//import java.util.*;
import java.awt.Color;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
//import java.io.*;

import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.border.LineBorder;
// import javax.xml.transform.Transformer;
// import javax.xml.transform.TransformerConfigurationException;
// import javax.xml.transform.TransformerException;
// import javax.xml.transform.TransformerFactory;
// import javax.xml.transform.dom.DOMSource;
// import javax.xml.transform.stream.StreamResult;
// import org.w3c.dom.Document;

public class CreateTables {
	
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
	
	public static void updateSQL(Connection conn, String QueryTorun) {
		Statement stmt;
		try {
			stmt = conn.createStatement();
			stmt.executeUpdate(QueryTorun);
			stmt.close();
			System.out.print("Update Success\n");
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
		dbTest = dbTest + serverName + ":"+portNum+"/";
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
			
			//below create a database named project1B
			System.out.print("--- creating database coms561project1b --- \n");
			updateSQL(conn, "drop database if exists coms561project1b;");
			updateSQL(conn, "create database coms561project1b;");
			updateSQL(conn, "use coms561project1b;");
			
			//remove foreign key check, to drop table if exist
			updateSQL(conn, "Set FOREIGN_KEY_CHECKS=0;");
			
			//from here onwards, create table for students, departments, degrees, 
			//courses, register, major and minor 
			System.out.print("--- creating table students --- \n");
			updateSQL(conn, "drop table if exists students;");
			updateSQL(conn, "create table students (\r\n"
					+ "snum int,\r\n"
					+ "ssn int,\r\n"
					+ "name varchar(10),\r\n"
					+ "gender varchar(1),\r\n"
					+ "dob datetime,\r\n"
					+ "c_addr varchar(20),\r\n"
					+ "c_phone varchar(10),\r\n"
					+ "p_addr varchar(20),\r\n"
					+ "p_phone varchar(10),\r\n"
					+ "PRIMARY KEY (ssn), \r\n"
					+ "UNIQUE (snum)\r\n"
					+ ");");

			System.out.print("--- creating table departments --- \n");
			updateSQL(conn, "drop table if exists departments;");
			updateSQL(conn, "create table departments (\r\n"
					+ "code int,\r\n"
					+ "name varchar(50),\r\n"
					+ "phone varchar(10),\r\n"
					+ "college varchar(20),\r\n"
					+ "PRIMARY KEY (code),\r\n"
					+ "UNIQUE (name)\r\n"
					+ ");");

			System.out.print("--- creating table degrees --- \n");
			updateSQL(conn, "drop table if exists degrees;");
			updateSQL(conn, "create table degrees (\r\n"
					+ "name varchar(50),\r\n"
					+ "level varchar(5),\r\n"
					+ "department_code int,\r\n"
					+ "PRIMARY KEY (name, level),\r\n"
					+ "FOREIGN KEY (department_code) REFERENCES departments(code)\r\n"
					+ ");");

			System.out.print("--- creating table courses --- \n");
			updateSQL(conn, "drop table if exists courses;");
			updateSQL(conn, "create table courses (\r\n"
					+ "number int,\r\n"
					+ "name varchar(50),\r\n"
					+ "description varchar(50),\r\n"
					+ "credithours int,\r\n"
					+ "level varchar(20),\r\n"
					+ "department_code int,\r\n"
					+ "PRIMARY KEY (number),\r\n"
					+ "UNIQUE (name),\r\n"
					+ "FOREIGN KEY (department_code) REFERENCES departments(code)\r\n"
					+ ");");

			System.out.print("--- creating table register --- \n");
			updateSQL(conn, "drop table if exists register;");
			updateSQL(conn, "create table register (\r\n"
					+ "snum int, \r\n"
					+ "course_number int, \r\n"
					+ "regtime varchar(20),\r\n"
					+ "grade int,\r\n"
					+ "PRIMARY KEY (snum, course_number),\r\n"
					+ "FOREIGN KEY (snum) REFERENCES students(snum),\r\n"
					+ "FOREIGN KEY (course_number) REFERENCES courses(number)\r\n"
					+ ");");

			System.out.print("--- creating table major --- \n");
			updateSQL(conn, "drop table if exists major;");
			updateSQL(conn, "create table major (\r\n"
					+ "snum int,\r\n"
					+ "name varchar(50),\r\n"
					+ "level varchar(5),\r\n"
					+ "PRIMARY KEY (snum, name, level),\r\n"
					+ "FOREIGN KEY (snum) REFERENCES students(snum),\r\n"
					+ "FOREIGN KEY (name, level) REFERENCES degrees(name, level)\r\n"
					+ ");");

			System.out.print("--- creating table minor --- \n");
			updateSQL(conn, "drop table if exists minor;");
			updateSQL(conn, "create table minor (\r\n"
					+ "snum int,\r\n"
					+ "name varchar(50),\r\n"
					+ "level varchar(5),\r\n"
					+ "PRIMARY KEY (snum, name, level),\r\n"
					+ "FOREIGN KEY (snum) REFERENCES students(snum),\r\n"
					+ "FOREIGN KEY (name, level) REFERENCES degrees(name, level)\r\n"
					+ ");");

			//return foreign key check, after all table created
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
