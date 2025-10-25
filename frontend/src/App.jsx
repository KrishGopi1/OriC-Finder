    import React, { useState } from 'react'
    import './index.css'

    export default function App(){
      const [file, setFile] = useState(null)
      const [seq, setSeq] = useState('')
      const [k, setK] = useState(9)
      const [windowSize, setWindowSize] = useState(500)
      const [loading, setLoading] = useState(false)
      const [result, setResult] = useState(null)
      const [error, setError] = useState(null)

      async function handleAnalyze(){
        setError(null)
        setLoading(true)
        setResult(null)
        const form = new FormData()
        form.append('k', k)
        form.append('window_size', windowSize)
        if (file) form.append('file', file)
        else form.append('sequence', seq)
        try {
          const res = await fetch('/analyze', { method: 'POST', body: form })
          if (!res.ok) {
            const err = await res.json()
            throw new Error(err.error || res.statusText)
          }
          const data = await res.json()
          setResult(data)
        } catch (e){
          setError(e.message)
        } finally {
          setLoading(false)
        }
      }

      return (
        <div className="app">
          <header className="hero">
            <h1>OriC Finder</h1>
            <p className="muted">Upload a genome FASTA or paste sequence — find predicted OriC and frequent k-mers.</p>
          </header>

          <section className="card">
            <div className="row">
              <label>Genome FASTA file</label>
              <input type="file" accept=".fa,.fna,.fasta,text/plain" onChange={e=>setFile(e.target.files[0])} />
            </div>
            <div className="muted or">OR paste sequence</div>
            <textarea value={seq} onChange={e=>setSeq(e.target.value)} placeholder=">chr1\nACTG..."></textarea>
            <div className="controls">
              <label>K-mer size <input type="number" value={k} onChange={e=>setK(parseInt(e.target.value||9))} min="1" /></label>
              <label>Window size <input type="number" value={windowSize} onChange={e=>setWindowSize(parseInt(e.target.value||500))} min="1" /></label>
              <button onClick={handleAnalyze} disabled={loading}>{loading? 'Analyzing...' : 'Analyze'}</button>
            </div>
          </section>

          {error && <div className="card error">{error}</div>}

          {result && <section className="card">
            <h2>Results</h2>
            <pre className="mono">
Genome length: {result.genome_length}
Predicted OriC center: {result.oric_center}
Minimum skew value: {result.min_skew_value}
Window: [{result.window_start}, {result.window_end}] (size {result.window_size})
            </pre>
            <div><strong>Most frequent k-mer(s):</strong> {result.most_frequent_kmers && result.most_frequent_kmers.length? result.most_frequent_kmers.join(', '): 'None'} (count: {result.kmer_count})</div>
            <div className="plot">
              <h3>Skew plot</h3>
              <img alt="skew" src={'data:image/png;base64,' + result.skew_plot} />
            </div>
          </section>}

          <footer className="muted"></footer>
        </div>
      )
    }
