from flask import Flask, request, jsonify, send_from_directory
import sys, io, base64
import matplotlib.pyplot as plt

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')

def parse_fasta(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    seq_lines = []
    for line in lines:
        if line.startswith('>'):
            continue
        seq_lines.append(line)
    seq = ''.join(seq_lines).upper()
    seq = ''.join([c for c in seq if c in set('ACGTN')])
    return seq

def gc_skew_finder(sequence):
    skew_values = [0]
    current_skew = 0
    for nucleotide in sequence:
        if nucleotide == 'G':
            current_skew += 1
        elif nucleotide == 'C':
            current_skew -= 1
        skew_values.append(current_skew)
    return skew_values

def min_skew_positions(skew_list):
    min_skew = sys.maxsize
    min_positions = []
    for i, skew in enumerate(skew_list):
        if skew < min_skew:
            min_skew = skew
            min_positions = [i]
        elif skew == min_skew:
            min_positions.append(i)
    return min_positions, min_skew

def freq_kmer(sequence, k):
    if k <= 0 or k > len(sequence):
        return [], 0
    kmer_count = {}
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k]
        kmer_count[kmer] = kmer_count.get(kmer, 0) + 1
    if not kmer_count:
        return [], 0
    max_count = max(kmer_count.values())
    frequent_kmers = [kmer for kmer, count in kmer_count.items() if count == max_count]
    return frequent_kmers, max_count

def plot_skew(skew_list, max_points=1000):
    # plot up to max_points to keep image small
    arr = skew_list[:max_points]
    plt.figure(figsize=(8,3))
    plt.plot(arr, linewidth=1.2)
    plt.fill_between(range(len(arr)), arr, alpha=0.07)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.form
    k = int(data.get('k', 9))
    window_size = int(data.get('window_size', 500))
    seq_text = ''
    if 'file' in request.files:
        f = request.files['file']
        seq_text = f.read().decode('utf-8', errors='ignore')
    else:
        seq_text = data.get('sequence', '')
    genome = parse_fasta(seq_text)
    if not genome:
        return jsonify({'error':'No valid sequence provided.'}), 400
    skew_array = gc_skew_finder(genome)
    min_pos, min_val = min_skew_positions(skew_array)
    oric_center = min_pos[0]
    start = max(0, oric_center - window_size//2)
    end = min(len(genome), oric_center + window_size//2)
    oric_region = genome[start:end]
    most_frequent, count = freq_kmer(oric_region, k)
    img_b64 = plot_skew(skew_array, max_points=2000)
    result = {
        'genome_length': len(genome),
        'oric_center': oric_center,
        'min_skew_value': min_val,
        'window_start': start,
        'window_end': end,
        'k': k,
        'window_size': window_size,
        'most_frequent_kmers': most_frequent,
        'kmer_count': count,
        'skew_plot': img_b64
    }
    return jsonify(result)
    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
