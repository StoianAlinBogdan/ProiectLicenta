from Helpers import generate_descriptive_stats
import Generators as gens
import pandas as pd

circuits = [
        'Hadamard1Bit', 'Hadamard8Bit', 'RY1Bit', 'RY8Bit', 'Uniform1Bit' ,'Uniform8Bit'
]

dict_for_csv = {
    'Generator': [],
    'Average': [],
    'KS Test': [],
    'Z Test': [],
    'Chi Squared Test': [],
    'Product of successive values': [],
    'Correlation Coefficient': []
}

def append_data(name, stats):
    dict_for_csv['Generator'].append(name)
    dict_for_csv['Average'].append(stats['mean'])
    dict_for_csv['KS Test'].append(stats['Kologomorov-Smirnov test vs. uniform (value should be very close to 0 for uniform):'])
    dict_for_csv['Z Test'].append(stats['Z-test vs. uniform (Value should be <-2.5 or >2.5: '])
    dict_for_csv['Chi Squared Test'].append(stats['Chi squared test for uniformity (Value should be close to 1 for uniform): '])
    dict_for_csv['Product of successive values'].append(stats['Product of successive values (should be 1/4 for uniform): '])
    dict_for_csv['Correlation Coefficient'].append(stats['Correlation coefficient (should be 0 for uniform): '])


if __name__ == "__main__":
    QRNGs = gens.QRNG()
    PRNGs = gens.PRNG()
    for i in range(100):
        print(i)
        for circuit in circuits:
            nums = QRNGs.run_circuit(circuit, 100000)
            stats = generate_descriptive_stats(nums)
            append_data(circuit, stats)
        nums = PRNGs.run_LCG(100000)
        stats = generate_descriptive_stats(nums)
        append_data('LCG', stats)
        nums = PRNGs.run_KISS(100000)
        stats = generate_descriptive_stats(nums)
        append_data('KISS', stats)

    df = pd.DataFrame.from_dict(dict_for_csv)
    df.to_csv('./Statistics.csv', index=False, header=True)