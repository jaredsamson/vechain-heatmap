function reachOut() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const processedColumn = 4; // Column D for "Status"
  const lastRow = sheet.getLastRow();

  // Start from row 2 to skip the header
  for (let i = 2; i <= lastRow; i++) {
    const status = sheet.getRange(i, processedColumn).getValue(); // Check if row is already processed
    if (status === 'Processed') {
      continue; // Skip already processed rows
    }

    const name = sheet.getRange(i, 1).getValue();
    const email = sheet.getRange(i, 2).getValue();
    const subject = sheet.getRange(i, 3).getValue();
    const additionalText = sheet.getRange(i, 5).getValue(); // Column E for Additional Text

    // Construct the email body with personalized details
    // <li> means bulletpoint 
    // Your special message comes right after. 
    const emailBody = `
      <div style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>Hello ${name},</h2>
        <p>I hope this message finds you well.</p>
        <p>We are excited to share some amazing news with you:</p>
        <ul>
          <li>Line 1 of exciting info</li>  
          <li>Line 2 with even more details</li>
        </ul>
        <p>${additionalText}</p>
        <p>Thank you for taking the time to read this. Feel free to reach out if you have any questions!</p>
        <p>Best regards,<br>Your Team</p>
        <img src="https://example.com/path-to-your-image.jpg" alt="Company Logo" style="width: 200px; height: auto; margin-top: 20px;">
      </div>
    `;

    try {
      GmailApp.sendEmail(email, subject, '', {
        htmlBody: emailBody,
      });
      sheet.getRange(i, processedColumn).setValue('Processed'); // Mark the row as processed
      console.log(`Email sent to ${email}`);
    } catch (error) {
      console.log(`Error sending email to ${email}: ${error.message}`);
    }
  }
}
