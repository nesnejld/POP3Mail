/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;
import java.util.Properties;

import org.apache.commons.net.PrintCommandListener;
import org.apache.commons.net.pop3.POP3Client;
import org.apache.commons.net.pop3.POP3MessageInfo;
import org.apache.commons.net.pop3.POP3SClient;
import org.json.JSONObject;

/**
 * This is an example program demonstrating how to use the POP3[S]Client class.
 * This program connects to a POP3[S] server and retrieves the message headers
 * of all the messages, printing the From: and Subject: header entries for each
 * message.
 * <p>
 * Usage: POP3Mail <pop3[s] server hostname> <username> <password> [secure
 * protocol, e.g. TLS]
 * <p>
 */
public final class POP3Mail {
	public static final Calendar calender = Calendar.getInstance();
	public static DateFormat dateformat = new SimpleDateFormat(
			"dd MMM yyyy HH:mm:ss");

	private static String escape(String s) {
		// return s.replaceAll("'", "\\\\\"");
		// return s.replaceAll("\"", "'");
		return s;
	}

	private static final String[] parseTo(String to) {
		String[] tokens = to.split(",");
		String[] results = new String[tokens.length];
		int i = 0;
		for (String t : tokens) {
			t = t.trim();
			if (t.startsWith("\"")) {
				t = t.substring(t.indexOf('"', 1) + 1);
			}
			if (t.indexOf("<") != -1) {
				results[i] = t.substring(t.indexOf("<") + 1,
						(t + ">").indexOf(">"));
			} else {
				results[i] = t;
			}
			++i;
		}
		return results;
	}

	public static final boolean printMessageInfo(BufferedReader reader, int id,
			PrintWriter printWriter) throws IOException {
		String from = "";
		String subject = "";
		String received = "";
		String to = "";
		String replyto = "";
		String date = "";
		String line = null;
		Date d = null;
		Date dd = null;
		try {
			dd = dateformat.parse("01 Jan 2020 00:00:00");
		} catch (ParseException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		while (true) {
			if (line == null) {
				line = reader.readLine();
			}
			if (line == null) {
				break;
			}
			String lower = line.toLowerCase(Locale.ENGLISH);
			System.out.println(line);
			if (lower.startsWith("from: ")) {
				from = line.substring(6).trim();
				line = null;
			} else if (lower.startsWith("reply-to: ")) {
				replyto = line.substring("reply-to: ".length()).trim();
				line = null;
			} else if (lower.startsWith("to: ")) {
				to = line.substring(3).trim();
				while ((line = reader.readLine()) != null) {
					lower = line.toLowerCase(Locale.ENGLISH);
					if (line.startsWith(" ")) {
						to += line;
					} else {
						break;
					}
				}

			} else if (lower.startsWith("subject: ")) {
				subject = line.substring(9).trim();
				line = null;
			} else if (lower.startsWith("date: ")) {
				date = line.substring("date: ".length()).trim();
				try {
					date = date.split(",")[1].trim();
					String[] tokens = date.split(" ");
					d = dateformat.parse(tokens[0] + " " + tokens[1] + " "
							+ tokens[2] + " " + tokens[3]);
				} catch (ParseException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				line = null;
			} else {
				line = null;
			}
		}
		if (d != null && d.before(dd)) {
			JSONObject jsonObject = new JSONObject();
			jsonObject.put("id", id);
			jsonObject.put("to", to);
			jsonObject.put("from", from);
			String[] t = parseTo(to);
			jsonObject.put("tolist", Arrays.asList(t));
			String ttt = "";
			for (String tt : t) {
				ttt += "," + tt;
			}
			String[] f = parseTo(from);
			String fff = "";
			for (String ff : f) {
				fff += "," + ff;
			}
			jsonObject.put("fromlist", Arrays.asList(f));
			jsonObject.put("subject", subject);
			jsonObject.put("date", date);
			jsonObject.put("time", d.getTime());
      jsonObject.put("reply-to", replyto);
			FileWriter fileWriter = new FileWriter(String.format(
					"../json/%05d.json", id));
			jsonObject.write(fileWriter);
			fileWriter.close();
			printWriter.println(String.format(
					"%d,'%s','%s','%s','%s','%s','%s','%s',%d", id,
					escape(from), fff.substring(1), escape(to),
					ttt.substring(1), escape(replyto), escape(subject), date,
					d.getTime()));
			return true;

		}
		return false;
	}

	public static void main(String[] args) {
		String server = null;
		String username = null;
		String password = null;
		if (new File("mail.properties").exists()) {
			Properties properties = new Properties();
			try {
				properties
						.load(new FileInputStream(new File("mail.properties")));
				server = properties.getProperty("server");
				username = properties.getProperty("username");
				password = properties.getProperty("password");
				ArrayList<String> list = new ArrayList<String>(
						Arrays.asList(new String[] { server, username, password }));
				list.addAll(Arrays.asList(args));
				args = list.toArray(new String[list.size()]);
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		if (args.length < 3) {
			System.err
					.println("Usage: POP3Mail <pop3 server hostname> <username> <password> [TLS [true=implicit]]");
			System.exit(1);
		}

		server = args[0];
		username = args[1];
		password = args[2];
		String proto = null;
		int messageid = -1;
		boolean implicit = false;
		for (int i = 3; i < args.length; ++i) {
			if (args[i].equals("-m")) {
				i += 1;
				messageid = Integer.parseInt(args[i]);
			}
		}

		// String proto = args.length > 3 ? args[3] : null;
		// boolean implicit = args.length > 4 ? Boolean.parseBoolean(args[4])
		// : false;

		POP3Client pop3;

		if (proto != null) {
			System.out.println("Using secure protocol: " + proto);
			pop3 = new POP3SClient(proto, implicit);
		} else {
			pop3 = new POP3Client();
		}
		pop3.setDefaultPort(110);
		System.out.println("Connecting to server " + server + " on "
				+ pop3.getDefaultPort());

		// We want to timeout if a response takes longer than 60 seconds
		pop3.setDefaultTimeout(60000);
		// suppress login details
		pop3.addProtocolCommandListener(new PrintCommandListener(
				new PrintWriter(System.out), true));

		try {
			pop3.connect(server);
		} catch (IOException e) {
			System.err.println("Could not connect to server.");
			e.printStackTrace();
			System.exit(1);
		}

		try {
			if (!pop3.login(username, password)) {
				System.err
						.println("Could not login to server.  Check password.");
				pop3.disconnect();
				System.exit(1);
			}
			PrintWriter printWriter = new PrintWriter(new FileWriter(
					"messages.csv"), true);
			POP3MessageInfo[] messages = null;
			if (messageid == -1) {
				messages = pop3.listMessages();
			} else {
				messages = new POP3MessageInfo[] { pop3.listMessage(messageid) };
			}
			if (messages == null) {
				System.err.println("Could not retrieve message list.");
				pop3.disconnect();
				return;
			} else if (messages.length == 0) {
				System.out.println("No messages");
				pop3.logout();
				pop3.disconnect();
				return;
			}
			new File("../json").mkdirs();
			for (POP3MessageInfo msginfo : messages) {
				BufferedReader reader = (BufferedReader) pop3
						.retrieveMessageTop(msginfo.number, 0);
				System.out.println(String.format("%d %s", msginfo.number,
						msginfo.identifier));
				if (reader == null) {
					System.err.println("Could not retrieve message header.");
					pop3.disconnect();
					System.exit(1);
				}
				if (printMessageInfo(reader, msginfo.number, printWriter)) {
				}
			}
			printWriter.close();
			pop3.logout();
			pop3.disconnect();
		} catch (IOException e) {
			e.printStackTrace();
			return;
		}
	}
}
