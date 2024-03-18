import csv

def convert_angles(input_filename, output_filename):
  """
  Reads angle values (assumed to be in the first column) from a CSV file,
  converts them from 0-360 to 0-7, and writes the results to a new CSV file.

  Args:
      input_filename (str): Path to the input CSV file.
      output_filename (str): Path to the output CSV file.
  """

  with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Read the header row (if present) and write it to the output file
    header = next(reader)
    writer.writerow(header)

    for row in reader:
      # Assuming angles are in the first column
      angle = float(row[1])
      new_angle = (angle / 360) * 6.4 # Scale and shift to 0-7 range

      # Wrap around if the angle exceeds 7
      new_angle = new_angle % 6.4

      # Update the first column with the converted angle and write the row
      row[1] = new_angle
      writer.writerow(row)

# Example usage (replace 'your_input.csv' and 'your_output.csv' with your actual filenames)
#convert_angles('lid2.csv', 'lid3.csv')
