import argparse
from nmap_scanner import NmapScanner
from cve_detection_metasploit_modules import exploit_cves, search_metasploit_for_cves
from database import DatabaseManager
from machine_learning import MachineLearningModel
from sklearn.externals import joblib 

def main():
    parser = argparse.ArgumentParser(description="Security Assessment Automation")
    parser.add_argument("--target", required=True, help="Target host")
    parser.add_argument("--train_model", action="store_true", help="Train the machine learning model")
    parser.add_argument("--load_model", action="store_true", help="Load the machine learning model and make predictions")

    args = parser.parse_args()

    if args.train_model:
        # Train the machine learning model
        ml = MachineLearningModel()
        data = DatabaseManager().load_data()
        X, y = ml.preprocess_data(data)
        model, _ = ml.train_model(X, y)
        ml.save_model(model)  # Save the trained model to a file
        ml.close()

    elif args.load_model:
        # Load the machine learning model and make predictions
        loaded_model = joblib.load('trained_model.pkl')  # Load the pre-trained model from a file
        target = args.target

        scanner = NmapScanner(target)
        scan_results = scanner.start_scan()
        predictions = []

        for target, service_data in scan_results.items():
            for service_info in service_data:
                service_name = service_info['name']
                service_version = service_info['version']
                port = service_info['port']

                # Make predictions using the loaded model
                prediction = loaded_model.predict([[service_name, service_version, port]])
                predictions.append((target, port, prediction))

        print("Machine Learning Predictions:")
        for prediction in predictions:
            target, port, prediction = prediction
            print(f"Target: {target}, Port: {port}, Prediction: {prediction}")

    else:
        # Perform scanning and exploitation
        target = args.target

        # Assuming Metasploit is running on 127.0.0.1
        scanner = NmapScanner(target)
        scan_results = scanner.start_scan()

        # The following code performs exploitation and stores results in the database
        for target, service_data in scan_results.items():
            for service_info in service_data:
                service_name = service_info['name']
                service_version = service_info['version']
                port = service_info['port']
                cve_list = service_info['cve_list']

                # Exploit CVEs
                exploitation_result = exploit_cves(target, service_name, service_version, port, cve_list)

                # Store results in the database
                DatabaseManager().store_exploitation_result(target, service_name, service_version, port, cve_list, exploitation_result)

if __name__ == '__main__':
    main()
