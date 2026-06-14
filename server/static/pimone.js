let TOTAL_CORES = 1;
let MAX_MEM_GB = 16;

const SAMPLE_INTERVAL_SEC = 3;
const MAX_HISTORY_SEC = 3600;
let chartWindowSec = 300;

const history = {
    labels: [],
    cpu: [],
    mem: []
};

// peaks within visible window
let maxCpuVisible = 0;
let maxMemVisible = 0;

// Combined line chart
const mainChart = new Chart(document.getElementById('main-chart'), {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'CPU %',
                data: [],
                borderColor: 'steelblue',
                fill: false,
                yAxisID: 'yCPU',
                pointRadius: ctx => {
                    const val = ctx.raw;
                    return val === maxCpuVisible ? 4 : 0;
                },
                pointBackgroundColor: ctx => {
                    const val = ctx.raw;
                    return val === maxCpuVisible ? 'red' : 'steelblue';
                }
            },
            {
                label: 'Mem GB',
                data: [],
                borderColor: 'seagreen',
                fill: false,
                yAxisID: 'yMem',
                pointRadius: ctx => {
                    const val = ctx.raw;
                    return val === maxMemVisible ? 4 : 0;
                },
                pointBackgroundColor: ctx => {
                    const val = ctx.raw;
                    return val === maxMemVisible ? 'red' : 'seagreen';
                }
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        scales: {
            yCPU: {
                type: 'linear',
                position: 'left',
                min: 0,
                max: 100,
                title: { display: true, text: 'CPU %', color: 'steelblue' }
            },
            yMem: {
                type: 'linear',
                position: 'right',
                min: 0,
                max: MAX_MEM_GB,
                title: { display: true, text: 'Mem GB', color: 'seagreen' },
                grid: { drawOnChartArea: false }
            }
        }
    }
});

// ── Doughnut gauge helper ────────────────────────────
function makeGauge(id, color) {
    return new Chart(document.getElementById(id), {
        type: 'doughnut',
        data: {
            datasets: [{ data: [0, 100], backgroundColor: [color, '#eee'], borderWidth: 0 }]
        },
        options: {
            responsive: true,
            circumference: 180,
            rotation: -90,
            cutout: '75%',
            plugins: { legend: { display: false }, tooltip: { enabled: false } }
        }
    });
}

const cpuGauge     = makeGauge('cpu-gauge',      'steelblue');
const memGauge     = makeGauge('mem-gauge',      'seagreen');
const diskGauge    = makeGauge('disk-gauge',     '#aa6c39');
const topprocGauge = makeGauge('topproc-gauge',  '#b22222');

function updateGauge(gauge, value, max) {
    const safeMax = max <= 0 ? 1 : max;
    const v = Math.min(Math.max(value, 0), safeMax);
    gauge.data.datasets[0].data = [v, safeMax - v];
    gauge.update();
}

// ── Update visible window from history ───────────────
function refreshChartWindow() {
    const maxPoints = Math.floor(chartWindowSec / SAMPLE_INTERVAL_SEC);
    const total = history.labels.length;
    const start = Math.max(total - maxPoints, 0);

    const labelsSlice = history.labels.slice(start);
    const cpuSlice    = history.cpu.slice(start);
    const memSlice    = history.mem.slice(start);

    maxCpuVisible = cpuSlice.length ? Math.max(...cpuSlice) : 0;
    maxMemVisible = memSlice.length ? Math.max(...memSlice) : 0;

    mainChart.data.labels = labelsSlice;
    mainChart.data.datasets[0].data = cpuSlice;
    mainChart.data.datasets[1].data = memSlice;
    mainChart.update();
}

// ── Push point into history ──────────────────────────
function pushPoint(label, cpuVal, memVal) {
    history.labels.push(label);
    history.cpu.push(cpuVal);
    history.mem.push(memVal);

    const maxPoints = Math.floor(MAX_HISTORY_SEC / SAMPLE_INTERVAL_SEC);
    if (history.labels.length > maxPoints) {
        history.labels.shift();
        history.cpu.shift();
        history.mem.shift();
    }

    refreshChartWindow();
}

// ── Window toggle handler ────────────────────────────
function setChartWindow(seconds, btn) {
    chartWindowSec = seconds;

    const buttons = btn.parentElement.querySelectorAll('.toggle-btn');
    buttons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    refreshChartWindow();
}

// ── Fetch + update everything ────────────────────────
function update() {
    fetch('/status')
        .then(res => res.json())
        .then(data => {
            const entries = Object.entries(data).sort((a, b) => a[0] - b[0]);
            if (!entries.length) return;

            const [ts, latest] = entries[entries.length - 1];

            console.log('overall cpu', latest.cpu.cpu);
            console.log('raw processes', latest.processes);

            // update TOTAL_CORES from backend once it's available
            if (latest.cores && Number.isFinite(latest.cores)) {
                TOTAL_CORES = latest.cores;
            }

            // update max mem (axis upper bound) from backend
            if (latest.memory && Number.isFinite(latest.memory.MemTotal)) {
                MAX_MEM_GB = latest.memory.MemTotal;
                mainChart.options.scales.yMem.max = MAX_MEM_GB;
            }

            const time = new Date(parseFloat(ts) * 1000).toLocaleTimeString();

            const cpu = latest.cpu.cpu;
            const mem = latest.memory.MemUsed;

            pushPoint(time, cpu, mem);

            // gauges: cpu & mem
            updateGauge(cpuGauge, cpu, 100);
            updateGauge(memGauge, mem, latest.memory.MemTotal);

            document.getElementById('cpu-gauge-label').textContent =
                `CPU: ${cpu.toFixed(1)}%`;
            document.getElementById('mem-gauge-label').textContent =
                `Mem: ${mem.toFixed(1)} / ${latest.memory.MemTotal} GB`;

            // processes
            // v[4] = proc_usage_perc (0–100 = 0–1 core on average)
            // v[3] = mem % as you had it
            const procs = Object.entries(latest.processes)
                .map(([pid, v]) => ({
                    pid,
                    name: v[0],
                    corePctAvg: v[4],
                    mem: v[3]
                }))
                .sort((a, b) => b.corePctAvg - a.corePctAvg)
                .slice(0, 10);

            document.getElementById('process-rows').innerHTML = procs.map(p => {
                const cpuTotalPct = p.corePctAvg / TOTAL_CORES;
                return `<tr>
                               <td>${p.pid}</td>
                               <td>${p.name}</td>
                               <td>${cpuTotalPct.toFixed(2)}</td>
                               <td>${p.mem.toFixed(1)}</td>
                            </tr>`;
            }).join('');

            // disk table
            document.getElementById('disk-rows').innerHTML = Object.entries(latest.disk)
                .map(([mount, d]) =>
                    `<tr><td>${mount}</td><td>${d.used[0]}</td><td>${d.total[0]}</td></tr>`
                ).join('');

            // disk gauge: use root '/'
            const root = latest.disk['/'];
            if (root) {
                const used = root.used[0];
                const total = root.total[0];
                const usedPct = total ? (used / total * 100) : 0;
                updateGauge(diskGauge, usedPct, 100);
                document.getElementById('disk-gauge-label').textContent =
                    `Disk /: ${usedPct.toFixed(1)}%`;
            } else {
                updateGauge(diskGauge, 0, 100);
                document.getElementById('disk-gauge-label').textContent = 'Disk /: n/a';
            }

            // top process gauge, normalized to total CPU
            if (procs.length) {
                const top = procs[0];
                const topCpuTotal = top.corePctAvg / TOTAL_CORES;
                const capped = Math.min(topCpuTotal, 100);
                updateGauge(topprocGauge, capped, 100);
                document.getElementById('topproc-gauge-label').textContent =
                    `Top: ${top.name} ${capped.toFixed(1)}% (avg)`;
            } else {
                updateGauge(topprocGauge, 0, 100);
                document.getElementById('topproc-gauge-label').textContent = 'Top proc: n/a';
            }
        });
}

update();
setInterval(update, SAMPLE_INTERVAL_SEC * 1000);

// ── Toggle sections ──────────────────────────────────
function toggleSection(sectionId, buttonId) {
    const section = document.getElementById(sectionId);
    const btn = document.getElementById(buttonId);
    const hidden = section.style.display === 'none';

    section.style.display = hidden ? 'block' : 'none';
    btn.classList.toggle('active', hidden);
}
